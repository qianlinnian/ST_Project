"""
测试生成器 - 主流程
职责：串联完整工作流：读取源代码 → 分析代码结构 → 构建 Prompt → 调用 LLM → 生成测试用例。
闭环反馈逻辑（覆盖率不足时补充生成）在模块6中集成。
"""

import os
import re
import json
from typing import Optional, Dict, Any, List

from src.analyzers.python_analyzer import PythonAnalyzer
from src.llm.client import LLMClient
from src.llm.prompts import build_python_prompt, build_general_prompt, build_supplement_prompt
from coverage.runner import CoverageRunner


# 语言扩展名映射
LANGUAGE_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".java": "java",
    ".cpp": "cpp",
    ".c": "c",
    ".go": "go",
}


class TestGenerator:
    """
    测试用例生成器
    完整流程：
      1. 读取源代码 → 2. 检测语言 → 3. AST分析（Python）或 LLM 通用分析
      → 4. 构建 Prompt → 5. 调用 LLM → 6. 解析响应 → 7. 生成可运行测试文件
      → 8. 运行覆盖率 → 9. 闭环补充（如需要） → 10. 保存输出
    """

    def __init__(self, source_path: str, requirement_path: Optional[str] = None,
                 llm_provider: str = "deepseek", config_path: str = "config.yaml",
                 max_rounds: int = 3, output_dir: str = "output"):
        """
        :param source_path: 被测源代码文件路径
        :param requirement_path: 可选，需求文档路径
        :param llm_provider: LLM 后端名称（deepseek / qwen / google / github）
        :param config_path: 配置文件路径
        :param max_rounds: 最大闭环轮次
        :param output_dir: 输出目录
        """
        self.source_path = source_path
        self.requirement_path = requirement_path
        self.llm_provider = llm_provider
        self.config_path = config_path
        self.max_rounds = max_rounds
        self.output_dir = output_dir

        # 读取源代码
        with open(source_path, "r", encoding="utf-8") as f:
            self.source_code = f.read()

        # 读取需求文档（可选）
        self.requirements = None
        if requirement_path:
            with open(requirement_path, "r", encoding="utf-8") as f:
                self.requirements = f.read()

        # 检测编程语言
        self.language = self._detect_language(source_path)

        # 初始化 LLM 客户端
        self.llm_client = LLMClient(provider=llm_provider, config_path=config_path)

    def _detect_language(self, path: str) -> str:
        """
        根据文件扩展名检测编程语言
        :param path: 文件路径
        :return: 语言名称字符串
        """
        ext = os.path.splitext(path)[1].lower()  # 获取扩展名，如 ".py"
        return LANGUAGE_MAP.get(ext, "unknown")

    def _analyze_code(self) -> Optional[Dict[str, Any]]:
        """
        分析源代码结构
        Python 用 AST 精确分析，其他语言返回 None（由 LLM 通用模式处理）
        :return: 分析结果字典，或 None
        """
        if self.language == "python":
            analyzer = PythonAnalyzer(self.source_code)
            return analyzer.analyze()
        return None

    def _build_prompt(self, analysis: Optional[Dict[str, Any]]) -> str:
        """
        根据语言和分析结果构建 prompt
        :param analysis: AST 分析结果（Python 有，其他语言为 None）
        :return: prompt 字符串
        """
        if self.language == "python" and analysis:
            # Python：使用 AST 分析结果构建详细 prompt
            return build_python_prompt(self.source_code, analysis, self.requirements)
        else:
            # 其他语言：使用通用 prompt，让 LLM 自行分析
            return build_general_prompt(self.source_code, self.language, self.requirements)

    def _parse_llm_response(self, response: str) -> List[Dict]:
        """
        从 LLM 响应文本中提取 JSON 测试用例数组
        LLM 可能返回 markdown 代码块包裹的 JSON，需要清理后解析。
        :param response: LLM 返回的原始文本
        :return: 测试用例列表
        """
        # 尝试提取 ```json ... ``` 代码块中的内容
        json_match = re.search(r'```(?:json)?\s*\n(.*?)\n```', response, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # 没有代码块，尝试直接找 JSON 数组
            json_str = response.strip()

        try:
            test_cases = json.loads(json_str)
            if isinstance(test_cases, list):
                return test_cases
            return [test_cases]  # 如果返回的是单个对象，包装为列表
        except json.JSONDecodeError:
            print(f"[警告] 无法解析 LLM 响应为 JSON，尝试宽松匹配...")
            # 宽松匹配：找到第一个 [ 到最后一个 ] 之间的内容
            bracket_match = re.search(r'\[.*\]', json_str, re.DOTALL)
            if bracket_match:
                try:
                    return json.loads(bracket_match.group())
                except json.JSONDecodeError:
                    pass
            print("[错误] 无法从 LLM 响应中提取测试用例")
            return []

    def _generate_test_file(self, test_cases: List[Dict]) -> str:
        """
        根据测试用例生成可运行的测试代码文件
        目前支持 Python（pytest 格式）
        :param test_cases: 测试用例列表
        :return: 测试代码字符串
        """
        if self.language == "python":
            return self._generate_pytest(test_cases)
        else:
            # 其他语言暂时返回测试用例的 JSON 描述
            return json.dumps(test_cases, indent=2, ensure_ascii=False)

    def _generate_pytest(self, test_cases: List[Dict]) -> str:
        """
        生成 pytest 格式的 Python 测试文件
        :param test_cases: 测试用例列表
        :return: pytest 测试代码
        """
        # 获取源文件的模块名（不含扩展名）
        module_name = os.path.splitext(os.path.basename(self.source_path))[0]

        # 提取所有函数名用于 import
        analysis = self._analyze_code()
        func_names = [f["name"] for f in analysis["functions"]] if analysis else []
        import_line = f"from {module_name} import {', '.join(func_names)}" if func_names else f"import {module_name}"

        # 构建测试方法
        test_methods = []
        for tc in test_cases:
            tc_id = tc.get("id", "TC000")
            desc = tc.get("description", "")
            input_data = tc.get("input", {})
            expected = tc.get("expected_output", "")

            # 生成方法名：取 id 转小写
            method_name = f"test_{tc_id.lower().replace('-', '_')}"
            # 构建输入参数字符串
            args_str = ", ".join(f"{k}={repr(v)}" for k, v in input_data.items()) if isinstance(input_data, dict) else repr(input_data)

            test_methods.append(f"""    def {method_name}(self):
        \"\"\"{tc_id}: {desc}\"\"\"
        # 输入: {input_data}
        # 期望输出: {expected}
        # TODO: 根据实际函数签名调整调用方式
        pass""")

        methods_str = "\n\n".join(test_methods)

        test_code = f"""\"\"\"自动生成的白盒测试用例 - {module_name}\"\"\"
import pytest
import sys
import os

# 将 targets 目录加入 path，以便导入被测模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'targets'))
{import_line}


class Test{module_name.title().replace('_', '')}:
    \"\"\"白盒测试类 - 由 LLM 自动生成\"\"\"

{methods_str}
"""
        return test_code

    def _save_outputs(self, test_cases: List[Dict], test_code: str,
                      analysis: Optional[Dict] = None,
                      coverage_report: Optional[Dict] = None) -> Dict[str, str]:
        """
        保存输出文件到 output 目录
        :param test_cases: 测试用例列表
        :param test_code: 可运行的测试代码
        :param analysis: AST 分析结果（可选）
        :param coverage_report: 覆盖率报告（可选）
        :return: 保存的文件路径字典
        """
        os.makedirs(self.output_dir, exist_ok=True)

        module_name = os.path.splitext(os.path.basename(self.source_path))[0]
        saved_files = {}

        # 1. 保存结构化测试用例 JSON
        cases_path = os.path.join(self.output_dir, f"test_cases_{module_name}.json")
        result = {
            "source_file": os.path.basename(self.source_path),
            "language": self.language,
            "llm_provider": self.llm_provider,
            "llm_model": self.llm_client.model,
            "analysis": analysis,
            "test_cases": test_cases,
            "coverage": coverage_report,
        }
        with open(cases_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        saved_files["test_cases"] = cases_path

        # 2. 保存可运行的测试文件
        test_path = os.path.join(self.output_dir, f"test_{module_name}.py")
        with open(test_path, "w", encoding="utf-8") as f:
            f.write(test_code)
        saved_files["test_file"] = test_path

        return saved_files

    def run(self, no_coverage: bool = False) -> Dict[str, Any]:
        """
        执行完整流程（含闭环反馈）
        流程：
          1. 分析代码 → 2. 构建 Prompt → 3. 调用 LLM → 4. 解析响应
          → 5. 生成测试文件 → 6. 运行覆盖率 → 7. 如果不足，反馈补充 → 8. 保存输出
        :param no_coverage: 为 True 时跳过覆盖率闭环，只生成测试用例
        :return: 包含 test_cases, test_code, analysis, coverage, saved_files 的结果字典
        """
        # ---- 步骤1：分析代码结构 ----
        print(f"[1] 分析源代码: {self.source_path} (语言: {self.language})")
        analysis = self._analyze_code()

        # ---- 步骤2-4：首次 LLM 生成 ----
        print(f"[2] 构建 Prompt...")
        prompt = self._build_prompt(analysis)

        print(f"[3] 调用 LLM ({self.llm_provider})...")
        response = self.llm_client.chat(prompt)

        print(f"[4] 解析 LLM 响应...")
        test_cases = self._parse_llm_response(response)
        print(f"    生成了 {len(test_cases)} 个测试用例")

        # ---- 步骤5：生成测试文件 ----
        test_code = self._generate_test_file(test_cases)
        coverage_report = None

        # ---- 步骤6-7：闭环反馈（覆盖率检测 + 补充生成） ----
        if not no_coverage and self.language == "python":
            # 先保存测试文件，才能运行覆盖率
            module_name = os.path.splitext(os.path.basename(self.source_path))[0]
            temp_test_path = os.path.join(self.output_dir, f"test_{module_name}.py")
            os.makedirs(self.output_dir, exist_ok=True)
            with open(temp_test_path, "w", encoding="utf-8") as f:
                f.write(test_code)

            current_round = 1
            while current_round <= self.max_rounds:
                print(f"\n[闭环] 第 {current_round}/{self.max_rounds} 轮 - 运行覆盖率测量...")
                runner = CoverageRunner(self.source_path, temp_test_path, self.language)
                coverage_report = runner.run()

                stmt_cov = coverage_report.get("statement_coverage", 0)
                branch_cov = coverage_report.get("branch_coverage", 0)
                print(f"    语句覆盖率: {stmt_cov:.1f}%  分支覆盖率: {branch_cov:.1f}%")

                # 覆盖率达标（>=90%）或已达最大轮次，结束闭环
                if stmt_cov >= 90 and branch_cov >= 80:
                    print(f"    覆盖率达标，闭环结束。")
                    break

                if current_round >= self.max_rounds:
                    print(f"    已达最大轮次 {self.max_rounds}，闭环结束。")
                    break

                # 覆盖率不足，构建补充 prompt 再次调用 LLM
                print(f"    覆盖率不足，生成补充测试用例...")
                supplement_prompt = build_supplement_prompt(
                    self.source_code, coverage_report, test_cases
                )
                supplement_response = self.llm_client.chat(supplement_prompt)
                supplement_cases = self._parse_llm_response(supplement_response)
                print(f"    补充了 {len(supplement_cases)} 个测试用例")

                # 合并测试用例，重新生成测试文件
                test_cases.extend(supplement_cases)
                test_code = self._generate_test_file(test_cases)
                with open(temp_test_path, "w", encoding="utf-8") as f:
                    f.write(test_code)

                current_round += 1

        # ---- 步骤8：保存最终输出 ----
        print(f"\n[保存] 输出文件...")
        saved_files = self._save_outputs(test_cases, test_code, analysis, coverage_report)
        for name, path in saved_files.items():
            print(f"    {name}: {path}")

        return {
            "test_cases": test_cases,
            "test_code": test_code,
            "analysis": analysis,
            "coverage": coverage_report,
            "rounds": current_round if not no_coverage and self.language == "python" else 0,
            "saved_files": saved_files,
        }
