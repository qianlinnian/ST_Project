"""
白盒测试用例生成工具 - 命令行入口
使用 AST 代码分析 + LLM 大语言模型自动生成白盒测试用例。

用法示例：
  # 基本用法：用 DeepSeek 分析 Python 文件
  python main.py --source targets/example.py --llm deepseek

  # 附带需求文档
  python main.py --source targets/example.py --llm qwen --requirement docs/spec.txt

  # 对比多个 LLM 的效果
  python main.py --source targets/example.py --compare

  # 只生成测试用例，不运行覆盖率闭环
  python main.py --source targets/example.py --llm deepseek --no-coverage

  # 设置最大闭环轮次
  python main.py --source targets/example.py --llm deepseek --max-rounds 5
"""

import argparse
import time
import sys
import os

from src.generators.test_generator import TestGenerator
from src.experiment.tracker import ExperimentTracker


def interactive_mode():
    """
    交互式参数输入模式
    当直接运行 python main.py（不带任何参数）时进入此模式。
    每个参数都有默认值，直接回车即可使用默认值。
    """
    print("=" * 60)
    print("白盒测试用例生成工具 - 交互式配置")
    print("（直接回车使用默认值）")
    print("=" * 60)

    source = input(f"\n源文件路径 [targets/convert_number_to_words.py]: ").strip()
    source = source or "targets/convert_number_to_words.py"

    llm = input(f"LLM 后端 (deepseek/openai/google/github) [deepseek]: ").strip()
    llm = llm or "deepseek"

    requirement = input(f"需求文档路径（可选，直接回车跳过）: ").strip()
    requirement = requirement or None

    compare_input = input(f"是否对比所有 LLM？(y/n) [n]: ").strip().lower()
    compare = compare_input == "y"

    output = input(f"输出目录 [output]: ").strip()
    output = output or "output"

    no_cov_input = input(f"是否跳过覆盖率闭环？(y/n) [y]: ").strip().lower()
    no_coverage = no_cov_input != "n"  # 默认跳过

    max_rounds = input(f"最大闭环轮次 [3]: ").strip()
    max_rounds = int(max_rounds) if max_rounds else 3

    config = input(f"配置文件路径 [config.yaml]: ").strip()
    config = config or "config.yaml"

    use_ast_input = input(f"是否使用 AST 分析辅助？(y/n) [n]: ").strip().lower()
    use_ast = use_ast_input == "y"

    # 构造与 argparse 兼容的命名空间对象
    args = argparse.Namespace(
        source=source, llm=llm, requirement=requirement,
        compare=compare, output=output, no_coverage=no_coverage,
        max_rounds=max_rounds, config=config, ast=use_ast
    )
    return args


def main():
    # ---- 解析命令行参数 ----
    parser = argparse.ArgumentParser(
        description="白盒测试用例生成工具 - AST分析 + LLM 自动生成"
    )
    parser.add_argument(
        "--source",
        help="被测源代码文件路径"
    )
    parser.add_argument(
        "--llm", default="deepseek",
        help="LLM 后端名称：deepseek / openai / google / github（默认 deepseek）"
    )
    parser.add_argument(
        "--requirement",
        help="可选的需求文档路径，为 LLM 提供额外上下文"
    )
    parser.add_argument(
        "--compare", action="store_true",
        help="用所有已配置的 LLM 运行并输出对比表格"
    )
    parser.add_argument(
        "--output", default="output",
        help="输出目录（默认 ./output）"
    )
    parser.add_argument(
        "--no-coverage", action="store_true",
        help="只生成测试用例，不运行覆盖率闭环"
    )
    parser.add_argument(
        "--max-rounds", type=int, default=3,
        help="最大闭环轮次（默认 3）"
    )
    parser.add_argument(
        "--config", default="config.yaml",
        help="配置文件路径（默认 config.yaml）"
    )
    parser.add_argument(
        "--ast", action="store_true",
        help="使用 AST 分析辅助生成（仅 Python 有效，默认不使用）"
    )

    args = parser.parse_args()

    # 如果没有指定 --source，进入交互模式
    if not args.source:
        args = interactive_mode()

    # ---- 检查源文件是否存在 ----
    if not os.path.exists(args.source):
        print(f"[错误] 源文件不存在: {args.source}")
        sys.exit(1)

    # ---- 对比模式：用所有 LLM 运行 ----
    if args.compare:
        run_compare(args)
    else:
        # 单次运行
        run_single(args)


def run_single(args) -> dict:
    """
    单次运行：用指定的 LLM 生成测试用例
    """
    print(f"=" * 60)
    print(f"白盒测试用例生成工具")
    print(f"源文件: {args.source}")
    print(f"LLM: {args.llm}")
    print(f"需求文档: {args.requirement or '无'}")
    print(f"输出目录: {args.output}")
    print(f"对比模式: {'是' if args.compare else '否'}")
    print(f"最大闭环轮次: {args.max_rounds}")
    print(f"闭环: {'关闭' if args.no_coverage else f'开启（最多 {args.max_rounds} 轮）'}")
    print(f"=" * 60)

    start_time = time.time()

    # 创建生成器并运行
    generator = TestGenerator(
        source_path=args.source,
        requirement_path=args.requirement,
        llm_provider=args.llm,
        config_path=args.config,
        max_rounds=args.max_rounds,
        output_dir=args.output,
        use_ast=args.ast,
    )
    result = generator.run(no_coverage=args.no_coverage)

    duration = time.time() - start_time

    # 记录实验数据
    tracker = ExperimentTracker(
        data_path=os.path.join(args.output, "experiment_data.json")
    )
    coverage = result.get("coverage") or {}
    test_results = coverage.get("test_results", {})
    tracker.record({
        "llm_provider": args.llm,
        "llm_model": generator.llm_client.model,
        "source_file": os.path.basename(args.source),
        "test_count": len(result["test_cases"]),
        "duration": duration,
        "rounds": result.get("rounds", 0),
        "statement_coverage": coverage.get("statement_coverage", 0),
        "branch_coverage": coverage.get("branch_coverage", 0),
        "passed": test_results.get("passed", 0),
        "failed": test_results.get("failed", 0),
    })

    print(f"\n[完成] 总耗时: {duration:.1f}s")
    return result


def run_compare(args):
    """
    对比模式：用所有已配置的 LLM 依次运行，输出对比表格
    """
    import yaml

    # 读取配置文件中的所有 LLM 后端
    with open(args.config, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    providers = list(config.get("llm", {}).keys())
    print(f"对比模式：将使用以下 LLM 后端运行: {', '.join(providers)}")
    print(f"=" * 60)

    for provider in providers:
        print(f"\n{'=' * 60}")
        print(f"▶ 使用 {provider} 运行...")
        print(f"{'=' * 60}")

        args.llm = provider
        try:
            run_single(args)
        except Exception as e:
            print(f"[错误] {provider} 运行失败: {e}")

    # 输出对比表格
    tracker = ExperimentTracker(
        data_path=os.path.join(args.output, "experiment_data.json")
    )
    print(f"\n{'=' * 60}")
    print("实验对比结果")
    print(f"{'=' * 60}")
    print(tracker.compare(source_file=os.path.basename(args.source)))

    # 保存 Markdown 报告
    report_path = os.path.join(args.output, "comparison_report.md")
    tracker.save_report(report_path, format="markdown")
    print(f"\n对比报告已保存: {report_path}")


if __name__ == "__main__":
    main()
