"""
统一 LLM 调用客户端
职责：提供统一接口，调用不同的 LLM API。
- DeepSeek、openai、GitHub Models：兼容 OpenAI API 格式，用 openai 库调用
- Google Gemini：使用 google-generativeai 库单独处理
"""

import os
import yaml
from openai import OpenAI
from typing import Optional, Union

# 设置代理（用于访问 Google 等需要代理的服务）
os.environ.setdefault("HTTP_PROXY", "http://127.0.0.1:7894")
os.environ.setdefault("HTTPS_PROXY", "http://127.0.0.1:7894")

import google.generativeai as genai


class LLMClient:
    """
    统一 LLM 客户端
    根据 provider 类型自动选择调用方式：
    - OpenAI 兼容后端（deepseek, openai, github）：通过 openai 库
    - Google Gemini：通过 google-generativeai 库
    """

    def __init__(self, provider: str, config_path: str = "config.yaml",
                 api_key: Optional[str] = None, base_url: Optional[str] = None,
                 model: Optional[str] = None):
        """
        初始化 LLM 客户端
        :param provider: LLM 后端名称，如 "deepseek", "openai", "google", "github"
        :param config_path: 配置文件路径，默认为 config.yaml
        :param api_key: 可选，手动指定 API Key（优先于配置文件）
        :param base_url: 可选，手动指定 API 地址（优先于配置文件）
        :param model: 可选，手动指定模型名（优先于配置文件）
        """
        self.provider = provider

        # 从配置文件加载该 provider 的设置
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        provider_config = config.get("llm", {}).get(provider, {})

        # 手动传入的参数优先于配置文件
        self.api_key = api_key or provider_config.get("api_key", "")
        self.base_url = base_url or provider_config.get("base_url", "")
        self.model = model or provider_config.get("model", "")

        # 根据 provider 类型选择不同的客户端初始化方式
        if provider == "google":
            # Google Gemini 使用专用库
            genai.configure(api_key=self.api_key)
            self.gemini_model = genai.GenerativeModel(self.model)
            self.client = None  # 不使用 OpenAI 客户端
        else:
            # 其他后端（deepseek, openai, siliconflow, github）都兼容 OpenAI 格式
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
            )
            self.gemini_model = None

    def chat(self, prompt: str, temperature: float = 0.3) -> str:
        """
        发送 prompt 给 LLM，返回响应文本
        :param prompt: 用户 prompt
        :param temperature: 生成温度，越低越确定性（默认 0.3）
        :return: LLM 返回的文本内容
        """
        if self.provider == "google":
            return self._chat_gemini(prompt, temperature)
        else:
            return self._chat_openai(prompt, temperature)

    def _chat_openai(self, prompt: str, temperature: float) -> str:
        """
        通过 OpenAI 兼容接口调用 LLM（适用于 deepseek, openai, siliconflow, github）
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的白盒测试专家，擅长分析代码结构并生成高覆盖率的测试用例。"},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
            )
            # 提取返回文本
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"[{self.provider}] API 调用失败: {e}")

    def _chat_gemini(self, prompt: str, temperature: float) -> str:
        """
        通过 Google Gemini API 调用（Gemini 使用独立的 SDK）
        """
        # 将系统提示和用户 prompt 合并（Gemini 不支持 system role 的相同方式）
        full_prompt = "你是一个专业的白盒测试专家，擅长分析代码结构并生成高覆盖率的测试用例。\n\n" + prompt
        try:
            response = self.gemini_model.generate_content(
                full_prompt,
                generation_config={"temperature": temperature},
            )
            return response.text
        except Exception as e:
            error_msg = str(e)
            if "RESOURCE_EXHAUSTED" in error_msg or "429" in error_msg or "quota" in error_msg.lower():
                raise RuntimeError(f"[Google] API 免费额度已用完，请稍后重试或更换模型。详情: https://ai.google.dev/gemini-api/docs/rate-limits")
            elif "NOT_FOUND" in error_msg:
                raise RuntimeError(f"[Google] 模型 '{self.model}' 不存在，请检查 config.yaml 中的 model 配置")
            else:
                raise RuntimeError(f"[Google] API 调用失败: {error_msg}")
