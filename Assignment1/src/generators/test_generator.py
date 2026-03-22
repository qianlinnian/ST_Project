"""
测试生成器 - 主流程
职责：串联完整工作流：读取源代码 → 分析代码结构 → 构建 Prompt → 调用 LLM → 生成测试用例。
闭环反馈逻辑（覆盖率不足时补充生成）在模块6中集成。
"""

import os
import re
import json
import time
from typing import Optional, Dict, Any, List

from src.analyzers.python_analyzer import PythonAnalyzer
from src.llm.client import LLMClient
from src.llm.prompts import build_python_prompt, build_general_prompt, build_supplement_prompt
from src.coverage.runner import CoverageRunner


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
                 max_rounds: int = 3, output_dir: str = "output",
                 use_ast: bool = False):
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

        # 是否使用 AST 分析辅助
        self.use_ast = use_ast

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
        if self.use_ast and self.language == "python" and analysis:
            # 使用 AST 分析结果构建详细 prompt
            return build_python_prompt(self.source_code, analysis, self.requirements)
        # 通用 prompt，让 LLM 自行分析代码结构
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
        except json.JSONDecodeError as e:
            # 打印出错位置附近的内容，方便调试
            pos = e.pos if hasattr(e, 'pos') else -1
            if pos > 0:
                start = max(0, pos - 80)
                end = min(len(json_str), pos + 80)
                print(f"[警告] 第一次解析失败: {e}")
            else:
                print(f"[警告] 第一次解析失败: {e}")
            # 宽松匹配：找到第一个 [ 到最后一个 ] 之间的内容
            bracket_match = re.search(r'\[.*\]', json_str, re.DOTALL)
            if bracket_match:
                raw = bracket_match.group()
                try:
                    return json.loads(raw)
                except json.JSONDecodeError as e2:
                    print(f"[警告] 第二次解析失败: {e2}")
                    # 尝试修复被截断的 JSON：补全缺失的括号
                    # 统计未闭合的括号数
                    open_braces = raw.count('{') - raw.count('}')
                    open_brackets = raw.count('[') - raw.count(']')
                    # 移除最后一个不完整的对象（从最后一个 { 开始截断）
                    if open_braces > 0:
                        last_complete = raw.rfind('},')
                        if last_complete > 0:
                            raw = raw[:last_complete + 1]  # 保留到最后一个完整的 }
                        raw += '}' * max(0, open_braces - 1)  # 补齐剩余 }
                    raw += ']' * max(0, open_brackets)  # 补齐 ]
                    try:
                        result = json.loads(raw)
                        print(f"[修复] 成功修复截断的 JSON")
                        if isinstance(result, list):
                            return result
                        return [result]
                    except json.JSONDecodeError:
                        pass
            # 最后兜底：逐个提取 JSON 对象
            print("[警告] 尝试逐个提取 JSON 对象...")
            objects = re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', json_str, re.DOTALL)
            parsed = []
            for obj_str in objects:
                try:
                    parsed.append(json.loads(obj_str))
                except json.JSONDecodeError:
                    continue
            if parsed:
                print(f"[修复] 逐个提取成功，得到 {len(parsed)} 个测试用例")
                return parsed
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
        elif self.language == "javascript":
            return self._generate_jest(test_cases)
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

        # 从 AST 提取函数名和类信息
        import ast
        analysis = self._analyze_code()
        func_names = [f["name"] for f in analysis["functions"]] if analysis else []

        # 构建 class_info：函数名 → 所属类名（用于识别类方法）
        class_info = {}
        class_names = []
        try:
            tree = ast.parse(self.source_code)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_names.append(node.name)
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            class_info[item.name] = node.name
        except SyntaxError:
            pass

        # 构建 import 行：导入独立函数和类
        standalone_funcs = [f for f in func_names if f not in class_info]
        import_parts = standalone_funcs + class_names
        import_line = f"from {module_name} import {', '.join(import_parts)}" if import_parts else f"import {module_name}"

        # 构建测试方法
        test_methods = []
        for tc in test_cases:
            tc_id = tc.get("id", "TC000")
            desc = tc.get("description", "")

            # 生成方法名：取 id 转小写
            method_name = f"test_{tc_id.lower().replace('-', '_')}"

            # 根据测试用例生成测试体
            body = self._build_test_body(tc, func_names, class_info)

            test_methods.append(f"""    def {method_name}(self):
        \"\"\"{tc_id}: {desc}\"\"\"
{body}""")

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

    def _build_test_body(self, tc: Dict, func_names: List[str], class_info: Dict) -> str:
        """
        根据测试用例生成测试方法体
        从 description 中提取函数名，自动识别是否为类方法。
        :param tc: 完整的测试用例字典
        :param func_names: 被测模块中的函数名列表
        :param class_info: 函数名 → 所属类名的映射，如 {"max_value": "NumberingSystem"}
        :return: 缩进好的测试方法体代码
        """
        input_data = tc.get("input", {})
        expected = tc.get("expected_output", "")
        desc = tc.get("description", "")
        expected_str = str(expected)
        lines = []

        # 判断是否期望抛出异常
        is_exception = False
        exception_type = ""
        for exc in ["ValueError", "TypeError", "KeyError", "IndexError", "RuntimeError", "Exception"]:
            if exc in expected_str:
                is_exception = True
                exception_type = exc
                break

        # 从 description 中提取函数名（LLM 通常会在描述里提到被测函数）
        target_func = None
        for fn in func_names:
            if fn in desc:
                target_func = fn
                break
        # 如果描述中没有，尝试从 covered_paths 提取
        if not target_func:
            for path in tc.get("covered_paths", []):
                for fn in func_names:
                    if fn in str(path):
                        target_func = fn
                        break
                if target_func:
                    break
        # 兜底：默认用第一个函数
        if not target_func and func_names:
            target_func = func_names[0]

        if not target_func:
            lines.append(f"        # 输入: {input_data}")
            lines.append(f"        # 期望输出: {expected}")
            lines.append(f"        pass  # TODO: 根据实际函数签名调整")
            return "\n".join(lines)

        # 构建函数调用表达式（处理类方法）
        if target_func in class_info:
            call_prefix = f"{class_info[target_func]}.{target_func}"
        else:
            call_prefix = target_func

        # 构建参数（排除 cls/self 等特殊参数）
        if isinstance(input_data, dict):
            filtered = {k: v for k, v in input_data.items() if k not in ("cls", "self")}
            args = ", ".join(f"{repr(v)}" for v in filtered.values())
        else:
            args = repr(input_data)

        if is_exception:
            lines.append(f"        with pytest.raises({exception_type}):")
            lines.append(f"            {call_prefix}({args})")
        else:
            lines.append(f"        result = {call_prefix}({args})")
            # 保持期望值的原始类型（int/float/bool/None 不加引号）
            if isinstance(expected, (int, float, bool)) or expected is None:
                lines.append(f"        assert result == {repr(expected)}")
            else:
                lines.append(f"        assert result == {repr(expected_str)}")

        return "\n".join(lines)

    def _generate_jest(self, test_cases: List[Dict]) -> str:
        """
        生成 Jest 格式的 JavaScript 测试文件
        :param test_cases: 测试用例列表
        :return: Jest 测试代码
        """
        # 被测文件相对路径（从 output/ 到 targets/）
        source_basename = os.path.basename(self.source_path)
        module_name = os.path.splitext(source_basename)[0]
        relative_import = f"../targets/{source_basename}"

        test_blocks = []
        for tc in test_cases:
            tc_id = tc.get("id", "TC000")
            desc = tc.get("description", "")

            test_body = self._build_jest_test_body(tc, module_name)
            # 转义描述中的单引号，防止 JS 语法错误
            safe_desc = desc.replace("'", "\\'")
            test_blocks.append(f"  test('{tc_id}: {safe_desc}', () => {{\n{test_body}\n  }});")

        tests_str = "\n\n".join(test_blocks)

        test_code = f"""/**
 * 自动生成的白盒测试用例 - {module_name}
 */
const _{module_name}Module = require('{relative_import}');
const {module_name} = _{module_name}Module.default || _{module_name}Module;

describe('{module_name} 白盒测试', () => {{
{tests_str}
}});
"""
        return test_code

    def _build_jest_test_body(self, tc: Dict, module_name: str) -> str:
        """
        根据测试用例生成 Jest 测试方法体
        :param tc: 测试用例字典
        :param module_name: 模块名（如 index）
        :return: 缩进好的测试体代码
        """
        input_data = tc.get("input", {})
        expected = tc.get("expected_output", "")
        expected_str = str(expected)
        desc = tc.get("description", "")
        lines = []

        # 判断是否期望抛出异常
        is_exception = any(kw in expected_str.lower() for kw in
                          ["error", "throw", "exception", "invalid"])

        # 构建输入参数
        if isinstance(input_data, dict):
            args_list = list(input_data.values())
            args = ", ".join(json.dumps(v, ensure_ascii=False) if isinstance(v, str) else json.dumps(v) for v in args_list)
        elif isinstance(input_data, list):
            args = ", ".join(json.dumps(v) for v in input_data)
        else:
            args = json.dumps(input_data) if input_data != "" else ""

        # 默认调用方式：module_name(args)
        call_expr = f"{module_name}({args})"

        # 尝试从 description 中检测链式调用（如 .format(), .isValid()）
        import re
        method_match = re.search(r'\.(\w+)\(\)', desc)
        if method_match:
            method = method_match.group(1)
            call_expr = f"{module_name}({args}).{method}()"

        if is_exception:
            lines.append(f"    expect(() => {{ {call_expr}; }}).toThrow();")
        else:
            # 格式化期望值
            if isinstance(expected, bool):
                expected_js = "true" if expected else "false"
            elif isinstance(expected, (int, float)):
                expected_js = str(expected)
            elif expected is None:
                expected_js = "null"
            else:
                expected_js = json.dumps(expected_str, ensure_ascii=False)

            lines.append(f"    const result = {call_expr};")
            lines.append(f"    expect(result).toBe({expected_js});")

        return "\n".join(lines)

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
        # 复用闭环阶段的时间戳（如果有），否则生成新的
        timestamp = getattr(self, '_run_timestamp', None) or time.strftime("%Y%m%d_%H%M%S")
        saved_files = {}

        # 1. 保存结构化测试用例 JSON
        cases_path = os.path.join(self.output_dir, f"test_cases_{module_name}_{timestamp}.json")
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
        test_ext = ".js" if self.language == "javascript" else ".py"
        test_path = os.path.join(self.output_dir, f"test_{module_name}_{timestamp}{test_ext}")
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
        if not no_coverage and self.language in ("python", "javascript"):
            # 先保存测试文件，才能运行覆盖率
            module_name = os.path.splitext(os.path.basename(self.source_path))[0]
            self._run_timestamp = time.strftime("%Y%m%d_%H%M%S")
            test_ext = ".js" if self.language == "javascript" else ".py"
            temp_test_path = os.path.join(self.output_dir, f"test_{module_name}_{self._run_timestamp}{test_ext}")
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

                # 覆盖率达标（>=95%）或已达最大轮次，结束闭环
                if stmt_cov >= 95 and branch_cov >= 90:
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
            "rounds": current_round if not no_coverage and self.language in ("python", "javascript") else 0,
            "saved_files": saved_files,
        }
