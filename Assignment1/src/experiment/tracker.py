"""
实验数据记录与对比
职责：记录每次运行的数据（LLM 后端、测试用例数、覆盖率、耗时等），
     支持多次运行的对比输出（表格形式）。
"""

import os
import json
import time
from typing import Dict, Any, List, Optional


class ExperimentTracker:
    """
    实验记录器
    记录每次测试生成运行的关键数据，并提供对比功能。
    数据保存为 JSON 文件，可跨次运行积累。
    """

    def __init__(self, data_path: str = "output/experiment_data.json"):
        """
        :param data_path: 实验数据保存路径
        """
        self.data_path = data_path
        self.records: List[Dict[str, Any]] = []

        # 加载已有的实验数据（如果存在）
        if os.path.exists(data_path):
            with open(data_path, "r", encoding="utf-8") as f:
                self.records = json.load(f)

    def record(self, run_data: Dict[str, Any]) -> None:
        """
        记录一次运行的数据
        :param run_data: 运行数据字典，应包含以下字段：
            - llm_provider: LLM 后端名称
            - llm_model: 模型名
            - source_file: 被测源文件
            - test_count: 生成的测试用例数
            - duration: 耗时（秒）
            - rounds: 闭环轮次数
            - statement_coverage: 语句覆盖率
            - branch_coverage: 分支覆盖率
            - passed: 通过的测试数
            - failed: 失败的测试数
        """
        # 添加时间戳
        run_data["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
        self.records.append(run_data)
        self._save()

    def _save(self) -> None:
        """将实验数据保存到文件"""
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(self.records, f, indent=2, ensure_ascii=False)

    def compare(self, source_file: Optional[str] = None) -> str:
        """
        生成多次运行的对比表格（纯文本）
        :param source_file: 可选，只对比指定源文件的运行记录
        :return: 格式化的对比表格字符串
        """
        records = self.records
        if source_file:
            records = [r for r in records if r.get("source_file") == source_file]

        if not records:
            return "暂无实验记录。"

        # 表头
        header = f"{'测试项目':<35} {'LLM':<15} {'模型':<30} {'用例数':>6} {'耗时':>8} {'语句覆盖':>8} {'分支覆盖':>8} {'轮次':>4} {'通过/失败':>10}"
        separator = "-" * len(header)

        rows = [header, separator]
        for r in records:
            row = (
                f"{r.get('source_file', '-'):<35} "
                f"{r.get('llm_provider', '-'):<15} "
                f"{r.get('llm_model', '-'):<30} "
                f"{r.get('test_count', 0):>6} "
                f"{r.get('duration', 0):>7.1f}s "
                f"{r.get('statement_coverage', 0):>7.1f}% "
                f"{r.get('branch_coverage', 0):>7.1f}% "
                f"{r.get('rounds', 0):>4} "
                f"{r.get('passed', 0):>4}/{r.get('failed', 0):<4}"
            )
            rows.append(row)

        return "\n".join(rows)

    def save_report(self, path: str, format: str = "json") -> None:
        """
        导出实验报告
        :param path: 输出路径
        :param format: 格式，"json" 或 "markdown"
        """
        os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)

        if format == "markdown":
            # 导出为 Markdown 表格
            md = "# 实验对比报告\n\n"
            md += "| 测试项目 | LLM | 模型 | 用例数 | 耗时 | 语句覆盖 | 分支覆盖 | 轮次 | 通过/失败 | 时间 |\n"
            md += "|----------|-----|------|--------|------|----------|----------|------|-----------|------|\n"
            for r in self.records:
                md += (
                    f"| {r.get('source_file', '-')} "
                    f"| {r.get('llm_provider', '-')} "
                    f"| {r.get('llm_model', '-')} "
                    f"| {r.get('test_count', 0)} "
                    f"| {r.get('duration', 0):.1f}s "
                    f"| {r.get('statement_coverage', 0):.1f}% "
                    f"| {r.get('branch_coverage', 0):.1f}% "
                    f"| {r.get('rounds', 0)} "
                    f"| {r.get('passed', 0)}/{r.get('failed', 0)} "
                    f"| {r.get('timestamp', '-')} |\n"
                )
            with open(path, "w", encoding="utf-8") as f:
                f.write(md)
        else:
            # 导出为 JSON
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.records, f, indent=2, ensure_ascii=False)
