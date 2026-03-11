from __future__ import annotations

import ast
from dataclasses import dataclass


@dataclass
class CompileResult:
    code: str
    variable_map: dict[str, int]


class PythonToBrainfuckCompiler:
    def __init__(self) -> None:
        self.var_map: dict[str, int] = {}
        self.ptr = 0
        self.out: list[str] = []

    def compile(self, source: str) -> CompileResult:
        tree = ast.parse(source)
        self._discover_vars(tree)
        self.ptr = 0
        self.out = []

        for stmt in tree.body:
            self._compile_stmt(stmt)

        code = optimize_brainfuck("".join(self.out))
        return CompileResult(code=code, variable_map=dict(self.var_map))

    def _discover_vars(self, tree: ast.AST) -> None:
        names: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                if node.id not in names:
                    names.append(node.id)
        self.var_map = {name: i for i, name in enumerate(sorted(names))}

    @property
    def temp0(self) -> int:
        return len(self.var_map)

    @property
    def temp1(self) -> int:
        return len(self.var_map) + 1

    def _emit(self, s: str) -> None:
        self.out.append(s)

    def _move_to(self, cell: int) -> None:
        diff = cell - self.ptr
        if diff > 0:
            self._emit(">" * diff)
        elif diff < 0:
            self._emit("<" * (-diff))
        self.ptr = cell

    def _clear(self, cell: int) -> None:
        self._move_to(cell)
        self._emit("[-]")

    def _add_const(self, cell: int, value: int) -> None:
        self._move_to(cell)
        if value >= 0:
            self._emit("+" * value)
        else:
            self._emit("-" * (-value))

    def _set_const(self, cell: int, value: int) -> None:
        self._clear(cell)
        self._add_const(cell, value)

    def _copy_preserve(self, src: int, dst: int) -> None:
        t = self.temp0
        self._clear(dst)
        self._clear(t)
        self._move_to(src)
        self._emit("[")
        self._emit("-")
        self._move_to(dst)
        self._emit("+")
        self._move_to(t)
        self._emit("+")
        self._move_to(src)
        self._emit("]")
        self._move_to(t)
        self._emit("[")
        self._emit("-")
        self._move_to(src)
        self._emit("+")
        self._move_to(t)
        self._emit("]")

    def _add_from_preserve(self, src: int, dst: int) -> None:
        t = self.temp0
        self._clear(t)
        self._move_to(src)
        self._emit("[")
        self._emit("-")
        self._move_to(dst)
        self._emit("+")
        self._move_to(t)
        self._emit("+")
        self._move_to(src)
        self._emit("]")
        self._move_to(t)
        self._emit("[")
        self._emit("-")
        self._move_to(src)
        self._emit("+")
        self._move_to(t)
        self._emit("]")

    def _sub_from_preserve(self, src: int, dst: int) -> None:
        t = self.temp0
        self._clear(t)
        self._move_to(src)
        self._emit("[")
        self._emit("-")
        self._move_to(dst)
        self._emit("-")
        self._move_to(t)
        self._emit("+")
        self._move_to(src)
        self._emit("]")
        self._move_to(t)
        self._emit("[")
        self._emit("-")
        self._move_to(src)
        self._emit("+")
        self._move_to(t)
        self._emit("]")

    def _compile_stmt(self, stmt: ast.stmt) -> None:
        if isinstance(stmt, ast.Assign):
            if len(stmt.targets) != 1 or not isinstance(stmt.targets[0], ast.Name):
                raise ValueError("Only simple assignments to variables are supported")
            dst = self.var_map[stmt.targets[0].id]
            self._compile_assign_value(stmt.value, dst)
            return

        if isinstance(stmt, ast.While):
            if not isinstance(stmt.test, ast.Name):
                raise ValueError("while condition must be a variable name")
            cond_cell = self.var_map[stmt.test.id]
            self._move_to(cond_cell)
            self._emit("[")
            for sub in stmt.body:
                self._compile_stmt(sub)
            self._move_to(cond_cell)
            self._emit("]")
            return

        if isinstance(stmt, ast.If):
            if not isinstance(stmt.test, ast.Name):
                raise ValueError("if condition must be a variable name")
            cond_cell = self.var_map[stmt.test.id]
            self._move_to(cond_cell)
            self._emit("[")
            for sub in stmt.body:
                self._compile_stmt(sub)
            self._clear(cond_cell)
            self._move_to(cond_cell)
            self._emit("]")
            return

        raise ValueError(f"Unsupported statement: {type(stmt).__name__}")


    def _expr_uses_cell(self, expr: ast.expr, cell: int) -> bool:
        for node in ast.walk(expr):
            if isinstance(node, ast.Name) and self.var_map.get(node.id) == cell:
                return True
        return False

    def _compile_assign_value(self, expr: ast.expr, dst: int) -> None:
        if isinstance(expr, ast.Constant) and isinstance(expr.value, int):
            self._set_const(dst, expr.value)
            return

        if isinstance(expr, ast.Name):
            self._copy_preserve(self.var_map[expr.id], dst)
            return

        if isinstance(expr, ast.BinOp) and isinstance(expr.op, (ast.Add, ast.Sub)):
            if self._expr_uses_cell(expr, dst):
                self._copy_preserve(dst, self.temp1)
            self._clear(dst)
            self._accumulate(expr.left, dst, add=True)
            self._accumulate(expr.right, dst, add=isinstance(expr.op, ast.Add))
            return

        raise ValueError("Supported rhs: int, variable, var +/- int, var +/- var")

    def _accumulate(self, expr: ast.expr, dst: int, add: bool) -> None:
        if isinstance(expr, ast.Constant) and isinstance(expr.value, int):
            self._add_const(dst, expr.value if add else -expr.value)
            return
        if isinstance(expr, ast.Name):
            src = self.var_map[expr.id]
            if src == dst:
                src = self.temp1
            if add:
                self._add_from_preserve(src, dst)
            else:
                self._sub_from_preserve(src, dst)
            return
        raise ValueError("Arithmetic terms must be int or variable")


def optimize_brainfuck(code: str) -> str:
    prev = None
    cur = code
    while prev != cur:
        prev = cur
        cur = (
            cur.replace("<>", "")
            .replace("><", "")
            .replace("+-", "")
            .replace("-+", "")
            .replace("[]", "")
            .replace("[-][-]", "[-]")
        )
    return cur
