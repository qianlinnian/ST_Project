"""
Python AST 代码分析器
职责：解析 Python 源代码，提取白盒测试所需的代码结构信息，包括：
  - 函数列表（函数名、参数、起止行号）
  - 分支点（if/elif/else、for、while、try/except）
  - 复合条件（and/or 表达式，用于条件覆盖）
  - 执行路径（基于分支组合推导，用于路径覆盖）
"""

import ast
from typing import List, Dict, Any


class PythonAnalyzer:
    """
    Python AST 分析器
    通过 ast 模块将源代码解析为抽象语法树，然后遍历树节点提取结构信息。
    非 Python 语言不使用此类，而是让 LLM 充当"分析器"。
    """

    def __init__(self, source_code: str):
        """
        初始化分析器
        :param source_code: Python 源代码字符串
        """
        self.source_code = source_code
        self.tree = ast.parse(source_code)       # 将源代码解析为 AST
        self.lines = source_code.splitlines()     # 按行拆分，用于统计总行数

    def _safe_unparse(self, node: ast.AST) -> str:
        """尽量将 AST 节点反解析为可读字符串。"""
        try:
            return ast.unparse(node)
        except Exception:
            return ast.dump(node)

    def get_functions(self) -> List[Dict[str, Any]]:
        """
        提取所有函数定义
        遍历 AST 找到所有 FunctionDef 节点，收集函数名、参数列表、起止行号、装饰器。
        :return: 函数信息列表，每个元素包含 name, params, start_line, end_line, decorators
        """
        functions = []
        for node in ast.walk(self.tree):          # ast.walk 递归遍历所有节点
            if isinstance(node, ast.FunctionDef):
                # 收集参数名
                params = []
                for arg in node.args.args:
                    params.append(arg.arg)
                functions.append({
                    "name": node.name,                                          # 函数名
                    "params": params,                                           # 参数列表
                    "start_line": node.lineno,                                  # 起始行号
                    "end_line": node.end_lineno,                                # 结束行号
                    "decorators": [ast.dump(d) for d in node.decorator_list],   # 装饰器
                })
        return functions

    def get_branches(self) -> List[Dict[str, Any]]:
        """
        提取所有分支点
        识别四种分支结构：
          - if/elif/else：条件分支
          - for：for 循环（可能有 else 子句）
          - while：while 循环
          - try/except：异常处理分支
        :return: 分支信息列表
        """
        branches = []
        for node in ast.walk(self.tree):
            # ---- if 分支 ----
            if isinstance(node, ast.If):
                condition_str = ast.unparse(node.test)   # 将条件表达式反解析为字符串
                branches.append({
                    "type": "if",
                    "line": node.lineno,
                    "condition": condition_str,
                    "has_else": len(node.orelse) > 0,                            # 是否有 else
                    "has_elif": (len(node.orelse) == 1                           # 是否有 elif
                                 and isinstance(node.orelse[0], ast.If)),        # （else 里只有一个 if）
                })
            # ---- for 循环 ----
            elif isinstance(node, ast.For):
                branches.append({
                    "type": "for",
                    "line": node.lineno,
                    "iter": ast.unparse(node.iter),       # 迭代对象
                    "target": ast.unparse(node.target),   # 循环变量
                    "has_else": len(node.orelse) > 0,
                })
            # ---- while 循环 ----
            elif isinstance(node, ast.While):
                branches.append({
                    "type": "while",
                    "line": node.lineno,
                    "condition": ast.unparse(node.test),
                    "has_else": len(node.orelse) > 0,
                })
            # ---- try/except 异常处理 ----
            elif isinstance(node, ast.Try):
                # 收集所有 except 子句的异常类型
                handlers = []
                for handler in node.handlers:
                    handler_type = ast.unparse(handler.type) if handler.type else "bare"
                    handlers.append(handler_type)
                branches.append({
                    "type": "try",
                    "line": node.lineno,
                    "handlers": handlers,                              # 异常处理类型列表
                    "has_else": len(node.orelse) > 0,                  # 是否有 else（无异常时执行）
                    "has_finally": len(node.finalbody) > 0,            # 是否有 finally
                })
            # ---- match/case 模式匹配 ----
            elif isinstance(node, ast.Match):
                cases = []
                for case in node.cases:
                    cases.append({
                        "pattern": self._safe_unparse(case.pattern),
                        "guard": self._safe_unparse(case.guard) if case.guard else None,
                        "start_line": case.body[0].lineno if case.body else node.lineno,
                        "end_line": case.body[-1].end_lineno if case.body else node.lineno,
                    })
                branches.append({
                    "type": "match",
                    "line": node.lineno,
                    "subject": self._safe_unparse(node.subject),
                    "case_count": len(node.cases),
                    "cases": cases,
                })
        return branches

    def get_conditions(self) -> List[Dict[str, Any]]:
        """
        提取复合布尔条件（and/or 表达式）
        用于条件覆盖分析：每个子条件都需要分别取 True 和 False。
        例如 `if a > 0 and b < 10:` 会被拆分为两个子条件 `a > 0` 和 `b < 10`。
        :return: 复合条件信息列表
        """
        conditions = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.BoolOp):
                sub_conditions = [ast.unparse(v) for v in node.values]    # 拆分子条件
                op_type = "and" if isinstance(node.op, ast.And) else "or"
                conditions.append({
                    "line": node.lineno,
                    "operator": op_type,                    # 逻辑运算符：and / or
                    "expression": ast.unparse(node),        # 完整表达式字符串
                    "sub_conditions": sub_conditions,       # 子条件列表
                })
        return conditions

    def _get_function_paths(self, func_node: ast.FunctionDef) -> List[str]:
        """
        推导一个函数内的所有可能执行路径（基于分支组合）
        路径用字符串表示，格式如：L10→L12(T)→L15 表示从第10行开始，第12行条件为 True，到第15行
        :param func_node: 函数的 AST 节点
        :return: 路径字符串列表
        """
        paths = []
        self._trace_paths(func_node.body, f"L{func_node.lineno}", paths)
        return paths

    def _trace_paths(self, stmts: list, current_path: str, paths: list):
        """
        递归追踪语句块中的执行路径
        遇到分支（if/for/while）时分裂为多条路径，递归处理每条分支。
        :param stmts: 当前语句块
        :param current_path: 当前已构建的路径字符串
        :param paths: 收集所有完整路径的列表（输出参数）
        """
        for stmt in stmts:
            if isinstance(stmt, ast.If):
                # True 分支：条件成立，进入 if body
                true_path = f"{current_path}→L{stmt.lineno}(T)"
                self._trace_paths(stmt.body, true_path, paths)
                # False 分支：条件不成立，进入 else/elif 或跳过
                if stmt.orelse:
                    false_path = f"{current_path}→L{stmt.lineno}(F)"
                    self._trace_paths(stmt.orelse, false_path, paths)
                else:
                    # 没有 else，False 分支直接结束
                    false_path = f"{current_path}→L{stmt.lineno}(F)"
                    paths.append(false_path)
                return  # if 之后的语句已在各分支内处理
            elif isinstance(stmt, ast.For) or isinstance(stmt, ast.While):
                # 循环有两种路径：进入循环体(loop) 和 跳过循环(skip)
                loop_path = f"{current_path}→L{stmt.lineno}(loop)"
                skip_path = f"{current_path}→L{stmt.lineno}(skip)"
                self._trace_paths(stmt.body, loop_path, paths)
                if stmt.orelse:
                    self._trace_paths(stmt.orelse, skip_path, paths)
                else:
                    paths.append(skip_path)
                return
            elif isinstance(stmt, ast.Match):
                # match/case: 为每个 case 分裂一条路径
                for index, case in enumerate(stmt.cases, 1):
                    pattern = self._safe_unparse(case.pattern)
                    guard = f" if {self._safe_unparse(case.guard)}" if case.guard else ""
                    case_path = f"{current_path}→L{stmt.lineno}(case{index}: {pattern}{guard})"
                    if case.body:
                        self._trace_paths(case.body, case_path, paths)
                    else:
                        paths.append(case_path)
                return
            else:
                # 普通语句，追加到当前路径
                current_path = f"{current_path}→L{stmt.lineno}"
        # 语句块结束，记录完整路径
        paths.append(current_path)

    def analyze(self) -> Dict[str, Any]:
        """
        执行完整分析，返回结构化结果
        串联所有子分析方法，返回包含 functions, branches, conditions, paths, total_lines 的字典。
        :return: 完整的代码结构分析结果
        """
        functions = self.get_functions()
        branches = self.get_branches()
        conditions = self.get_conditions()

        # 为每个函数推导执行路径
        paths = {}
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                func_paths = self._get_function_paths(node)
                paths[node.name] = func_paths

        return {
            "functions": functions,       # 函数列表
            "branches": branches,         # 分支点列表
            "conditions": conditions,     # 复合条件列表
            "paths": paths,               # 各函数的执行路径
            "total_lines": len(self.lines),  # 源代码总行数
        }
