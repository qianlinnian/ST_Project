"""
测试运行 + 覆盖率测量
职责：运行生成的测试代码，测量覆盖率，返回结构化报告。
支持的语言：
  - Python：使用 pytest + coverage.py
  - JavaScript：使用 Jest + --coverage
"""

import os
import json
import subprocess
from typing import Dict, Any, List


class CoverageRunner:
    """
    覆盖率运行器
    运行测试文件，测量被测源代码的覆盖率，返回结构化的覆盖率报告。
    """

    def __init__(self, source_path: str, test_path: str, language: str = "python"):
        """
        :param source_path: 被测源代码路径
        :param test_path: 测试文件路径
        :param language: 编程语言（目前只支持 python）
        """
        self.source_path = os.path.abspath(source_path)
        self.test_path = os.path.abspath(test_path)
        self.language = language
        # 项目根目录（Assignment1）
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    def run(self) -> Dict[str, Any]:
        """
        运行测试并返回覆盖率报告
        :return: 包含 statement_coverage, branch_coverage, uncovered_lines 等的字典
        """
        if self.language == "python":
            return self._run_python_coverage()
        elif self.language == "javascript":
            return self._run_js_coverage()
        else:
            return {"error": f"暂不支持 {self.language} 语言的覆盖率测量"}

    def _run_python_coverage(self) -> Dict[str, Any]:
        """
        使用 coverage.py + pytest 运行 Python 测试并收集覆盖率
        步骤：
          1. coverage run -m pytest test_file.py  — 运行测试并收集覆盖率数据
          2. coverage json -o coverage.json       — 导出为 JSON 格式
          3. 解析 JSON 提取覆盖率信息
        """
        test_dir = os.path.dirname(self.test_path)
        source_file = os.path.basename(self.source_path)

        # 覆盖率数据文件的临时路径
        coverage_data = os.path.join(test_dir, ".coverage")
        coverage_json = os.path.join(test_dir, "coverage.json")

        # 步骤1：运行 pytest 并收集覆盖率
        run_cmd = [
            "python", "-m", "coverage", "run",
            "--source", os.path.dirname(self.source_path),  # 只测量被测文件所在目录
            "--branch",                                      # 启用分支覆盖
            "-m", "pytest", self.test_path,                  # 用 pytest 运行测试
            "-v",                                            # 显示详细输出
        ]

        print(f"  运行命令: {' '.join(run_cmd)}")
        result = subprocess.run(
            run_cmd,
            capture_output=True,
            text=True,
            cwd=test_dir,  # 在测试文件所在目录运行
        )

        # 收集 pytest 测试结果
        test_output = result.stdout + result.stderr
        test_results = self._parse_pytest_output(test_output)

        # 步骤2：导出覆盖率为 JSON
        json_cmd = [
            "python", "-m", "coverage", "json",
            "-o", coverage_json,
        ]
        subprocess.run(json_cmd, capture_output=True, text=True, cwd=test_dir)

        # 步骤3：解析覆盖率 JSON
        report = self._parse_coverage_json(coverage_json)
        report["test_results"] = test_results

        # 清理临时文件
        for f in [coverage_data, coverage_json]:
            if os.path.exists(f):
                os.remove(f)

        return report

    def _parse_pytest_output(self, output: str) -> Dict[str, int]:
        """
        从 pytest 输出中解析测试结果（通过/失败/错误数量）
        :param output: pytest 的标准输出
        :return: {"total": N, "passed": N, "failed": N, "error": N}
        """
        import re
        results = {"total": 0, "passed": 0, "failed": 0, "error": 0}

        # 匹配 pytest 结果行，如 "5 passed, 1 failed"
        match = re.search(r'(\d+) passed', output)
        if match:
            results["passed"] = int(match.group(1))

        match = re.search(r'(\d+) failed', output)
        if match:
            results["failed"] = int(match.group(1))

        match = re.search(r'(\d+) error', output)
        if match:
            results["error"] = int(match.group(1))

        results["total"] = results["passed"] + results["failed"] + results["error"]
        return results

    def _parse_coverage_json(self, json_path: str) -> Dict[str, Any]:
        """
        解析 coverage.py 生成的 JSON 报告
        :param json_path: coverage.json 文件路径
        :return: 结构化的覆盖率报告
        """
        if not os.path.exists(json_path):
            return {
                "statement_coverage": 0.0,
                "branch_coverage": 0.0,
                "uncovered_lines": [],
                "uncovered_branches": [],
            }

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # coverage.json 的结构：{"totals": {...}, "files": {"文件名": {...}}}
        totals = data.get("totals", {})

        # 提取各文件的未覆盖行和分支
        uncovered_lines = []
        uncovered_branches = []
        for file_path, file_data in data.get("files", {}).items():
            # missing_lines 是未执行的行号列表
            uncovered_lines.extend(file_data.get("missing_lines", []))
            # missing_branches 是未覆盖的分支，格式为 [[起始行, 目标行], ...]
            for branch in file_data.get("missing_branches", []):
                uncovered_branches.append(f"L{branch[0]} → L{branch[1]}")

        return {
            "statement_coverage": totals.get("percent_covered", 0.0),
            "branch_coverage": totals.get("percent_branches_covered", 0.0),
            "uncovered_lines": uncovered_lines,
            "uncovered_branches": uncovered_branches,
        }

    def _run_js_coverage(self) -> Dict[str, Any]:
        """
        使用 Jest + --coverage 运行 JavaScript 测试并收集覆盖率
        步骤：
          1. npx jest test_file.js --coverage --coverageReporters=json-summary
          2. 解析 coverage/coverage-summary.json
          3. 从 Jest 输出中解析测试通过/失败数量
        """
        # Jest 的覆盖率输出目录
        coverage_dir = os.path.join(self.project_root, "coverage")
        coverage_json_path = os.path.join(coverage_dir, "coverage-final.json")

        # 构建 Jest 命令（使用 json reporter 获取行级覆盖信息）
        source_rel = os.path.relpath(self.source_path, self.project_root).replace(os.sep, '/')
        test_file_pattern = self.test_path.replace("\\", "/")
        run_cmd = [
            "npx", "jest",
            "--testPathPattern", test_file_pattern,
            "--coverage",
            "--coverageReporters=json",
            f"--collectCoverageFrom={source_rel}",
            "--no-cache",
        ]

        print(f"  运行命令: {' '.join(run_cmd)}")
        result = subprocess.run(
            run_cmd,
            capture_output=True,
            text=True,
            cwd=self.project_root,
            shell=True,
            encoding="utf-8",
            errors="replace",
        )

        # 从 Jest 输出中解析 passed/failed 数量
        test_output = (result.stdout or "") + (result.stderr or "")
        test_results = self._parse_jest_output(test_output)

        # 解析覆盖率 JSON（行级信息从文件读取，不依赖控制台输出）
        report = self._parse_jest_coverage(coverage_json_path)
        report["test_results"] = test_results
        # 不保存 test_output 到报告（避免编码乱码，覆盖率信息已从 JSON 获取）

        # 清理覆盖率目录
        if os.path.exists(coverage_dir):
            import shutil
            shutil.rmtree(coverage_dir, ignore_errors=True)

        return report

    def _parse_jest_output(self, output: str) -> Dict[str, int]:
        """
        从 Jest 输出中解析测试结果
        Jest 输出格式如: "Tests:  2 failed, 18 passed, 20 total"
        """
        import re
        results = {"total": 0, "passed": 0, "failed": 0, "error": 0}

        match = re.search(r'Tests:\s+(?:(\d+)\s+failed,\s+)?(\d+)\s+passed', output)
        if match:
            if match.group(1):
                results["failed"] = int(match.group(1))
            results["passed"] = int(match.group(2))
        else:
            # 备用：只有 failed
            match = re.search(r'Tests:\s+(\d+)\s+failed', output)
            if match:
                results["failed"] = int(match.group(1))

        results["total"] = results["passed"] + results["failed"]
        return results

    def _parse_jest_coverage(self, json_path: str) -> Dict[str, Any]:
        """
        解析 Jest 生成的 coverage-final.json（json reporter）
        结构: {"文件绝对路径": {"statementMap": {...}, "s": {...}, "branchMap": {...}, "b": {...}}}
        从中提取语句/分支覆盖率和未覆盖的行号。
        """
        if not os.path.exists(json_path):
            return {
                "statement_coverage": 0.0,
                "branch_coverage": 0.0,
                "uncovered_lines": [],
                "uncovered_branches": [],
            }

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        total_stmts = 0
        covered_stmts = 0
        total_branches = 0
        covered_branches = 0
        uncovered_lines = []
        uncovered_branches = []

        for file_path, file_data in data.items():
            # 语句覆盖：s 是 {语句ID: 执行次数}，statementMap 是 {语句ID: {start: {line}, end: {line}}}
            stmt_map = file_data.get("statementMap", {})
            s = file_data.get("s", {})
            for stmt_id, count in s.items():
                total_stmts += 1
                if count > 0:
                    covered_stmts += 1
                else:
                    # 记录未覆盖的行号
                    loc = stmt_map.get(stmt_id, {})
                    start_line = loc.get("start", {}).get("line", 0)
                    if start_line and start_line not in uncovered_lines:
                        uncovered_lines.append(start_line)

            # 分支覆盖：b 是 {分支ID: [分支1执行次数, 分支2执行次数, ...]}
            branch_map = file_data.get("branchMap", {})
            b = file_data.get("b", {})
            for branch_id, counts in b.items():
                for i, count in enumerate(counts):
                    total_branches += 1
                    if count > 0:
                        covered_branches += 1
                    else:
                        loc = branch_map.get(branch_id, {})
                        line = loc.get("loc", {}).get("start", {}).get("line", 0)
                        branch_type = loc.get("type", "branch")
                        uncovered_branches.append(f"L{line}: {branch_type} branch-{i}")

        uncovered_lines.sort()

        stmt_pct = (covered_stmts / total_stmts * 100) if total_stmts > 0 else 0.0
        branch_pct = (covered_branches / total_branches * 100) if total_branches > 0 else 0.0

        return {
            "statement_coverage": round(stmt_pct, 2),
            "branch_coverage": round(branch_pct, 2),
            "uncovered_lines": uncovered_lines,
            "uncovered_branches": uncovered_branches,
        }

    def get_uncovered_lines(self) -> List[int]:
        """运行覆盖率并返回未覆盖的行号列表"""
        report = self.run()
        return report.get("uncovered_lines", [])

    def get_uncovered_branches(self) -> List[str]:
        """运行覆盖率并返回未覆盖的分支列表"""
        report = self.run()
        return report.get("uncovered_branches", [])
