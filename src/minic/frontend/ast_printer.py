from typing import Any, List, Tuple
from .ast_nodes import (
    ASTNode, Program, StructDecl, FieldDecl, VarDecl, FuncDecl, Param,
    Block, ExprStmt, IfStmt, WhileStmt, ForStmt, ReturnStmt,
    Literal, VarExpr, ArrayAccessExpr, FieldAccessExpr, CallExpr,
    UnaryExpr, BinaryExpr, AssignExpr, TypeSpec, ArraySuffix
)


class ASTPrinter:
    """Pretty prints MiniC Abstract Syntax Trees with indentation and graphical tree hierarchy."""

    def __init__(self, indent_size: int = 2):
        self.indent_size = indent_size

    def print_ast(self, node: ASTNode) -> str:
        """Indented text representation."""
        return self._format_node(node, 0)

    def print_tree(self, node: ASTNode) -> str:
        """Visual tree with branch glyphs (├──, └──, │)."""
        label, children = self._node_to_tree(node)
        lines: List[str] = [label]
        self._build_tree_lines(children, "", lines)
        return "\n".join(lines)

    def _build_tree_lines(self, children: List[Tuple[str, List[Any]]], prefix: str, lines: List[str]) -> None:
        count = len(children)
        for i, (child_label, grandchildren) in enumerate(children):
            is_last = (i == count - 1)
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{child_label}")
            sub_prefix = f"{prefix}{'    ' if is_last else '│   '}"
            self._build_tree_lines(grandchildren, sub_prefix, lines)

    def _node_to_tree(self, node: Any) -> Tuple[str, List[Tuple[str, List[Any]]]]:
        if node is None:
            return "None", []

        if isinstance(node, Program):
            children = [self._node_to_tree(d) for d in node.declarations]
            return f"Program (L{node.line})", children

        elif isinstance(node, StructDecl):
            children = [self._node_to_tree(f) for f in node.fields]
            return f"StructDecl: {node.name} (L{node.line})", children

        elif isinstance(node, FieldDecl):
            suffix = f" {node.array_suffix}" if node.array_suffix else ""
            return f"Field: {node.type_spec} {node.name}{suffix}", []

        elif isinstance(node, VarDecl):
            suffix = f" {node.array_suffix}" if node.array_suffix else ""
            children = []
            if node.init_expr:
                children.append(("Init", [self._node_to_tree(node.init_expr)]))
            return f"VarDecl: {node.type_spec} {node.name}{suffix} (L{node.line})", children

        elif isinstance(node, Param):
            suffix = f" {node.array_suffix}" if node.array_suffix else ""
            return f"Param: {node.type_spec} {node.name}{suffix}", []

        elif isinstance(node, FuncDecl):
            children = []
            if node.params:
                param_children = [self._node_to_tree(p) for p in node.params]
                children.append(("Params", param_children))
            body_label, body_children = self._node_to_tree(node.body)
            children.append((f"Body", body_children))
            return f"FuncDecl: {node.name} -> {node.return_type} (L{node.line})", children

        elif isinstance(node, Block):
            children = [self._node_to_tree(s) for s in node.statements]
            return f"Block (L{node.line})", children

        elif isinstance(node, ExprStmt):
            return f"ExprStmt (L{node.line})", [self._node_to_tree(node.expr)]

        elif isinstance(node, IfStmt):
            children = [("Condition", [self._node_to_tree(node.cond)])]
            _, then_children = self._node_to_tree(node.then_branch)
            children.append(("Then", then_children))
            if node.else_branch:
                _, else_children = self._node_to_tree(node.else_branch)
                children.append(("Else", else_children))
            return f"IfStmt (L{node.line})", children

        elif isinstance(node, WhileStmt):
            children = [
                ("Condition", [self._node_to_tree(node.cond)]),
                ("Body", [self._node_to_tree(node.body)])
            ]
            return f"WhileStmt (L{node.line})", children

        elif isinstance(node, ForStmt):
            children = []
            if node.init:
                children.append(("Init", [self._node_to_tree(node.init)]))
            if node.cond:
                children.append(("Condition", [self._node_to_tree(node.cond)]))
            if node.step:
                children.append(("Step", [self._node_to_tree(node.step)]))
            children.append(("Body", [self._node_to_tree(node.body)]))
            return f"ForStmt (L{node.line})", children

        elif isinstance(node, ReturnStmt):
            children = [self._node_to_tree(node.expr)] if node.expr else []
            return f"ReturnStmt (L{node.line})", children

        elif isinstance(node, Literal):
            return f"Literal({node.lit_type}: {node.value!r})", []

        elif isinstance(node, VarExpr):
            return f"Var({node.name})", []

        elif isinstance(node, ArrayAccessExpr):
            children = [("Target", [self._node_to_tree(node.target)])]
            for idx in node.indices:
                children.append(("Index", [self._node_to_tree(idx)]))
            return f"ArrayAccess (L{node.line})", children

        elif isinstance(node, FieldAccessExpr):
            return f"FieldAccess(.{node.field})", [self._node_to_tree(node.target)]

        elif isinstance(node, CallExpr):
            children = [self._node_to_tree(a) for a in node.args]
            return f"Call: {node.func_name}()", children

        elif isinstance(node, UnaryExpr):
            return f"Unary({node.op})", [self._node_to_tree(node.operand)]

        elif isinstance(node, BinaryExpr):
            children = [
                ("Left", [self._node_to_tree(node.left)]),
                ("Right", [self._node_to_tree(node.right)])
            ]
            return f"BinaryExpr({node.op})", children

        elif isinstance(node, AssignExpr):
            children = [
                ("Target", [self._node_to_tree(node.target)]),
                ("Value", [self._node_to_tree(node.value)])
            ]
            return f"Assign '=' (L{node.line})", children

        return f"{type(node).__name__}", []

    def _format_node(self, node: Any, depth: int) -> str:
        indent = " " * (depth * self.indent_size)
        if node is None:
            return f"{indent}None"
        if isinstance(node, Program):
            lines = [f"{indent}Program (L{node.line})"]
            for decl in node.declarations:
                lines.append(self._format_node(decl, depth + 1))
            return "\n".join(lines)
        elif isinstance(node, StructDecl):
            lines = [f"{indent}StructDecl: {node.name} (L{node.line})"]
            for f in node.fields:
                lines.append(self._format_node(f, depth + 1))
            return "\n".join(lines)
        elif isinstance(node, FieldDecl):
            suffix_str = f" {node.array_suffix}" if node.array_suffix else ""
            return f"{indent}FieldDecl: {node.type_spec} {node.name}{suffix_str} (L{node.line})"
        elif isinstance(node, VarDecl):
            suffix_str = f" {node.array_suffix}" if node.array_suffix else ""
            lines = [f"{indent}VarDecl: {node.type_spec} {node.name}{suffix_str} (L{node.line})"]
            if node.init_expr:
                lines.append(f"{indent}  Init:")
                lines.append(self._format_node(node.init_expr, depth + 2))
            return "\n".join(lines)
        elif isinstance(node, Param):
            suffix_str = f" {node.array_suffix}" if node.array_suffix else ""
            return f"{indent}Param: {node.type_spec} {node.name}{suffix_str} (L{node.line})"
        elif isinstance(node, FuncDecl):
            lines = [f"{indent}FuncDecl: {node.name} -> {node.return_type} (L{node.line})"]
            if node.params:
                lines.append(f"{indent}  Params:")
                for p in node.params:
                    lines.append(self._format_node(p, depth + 2))
            lines.append(f"{indent}  Body:")
            lines.append(self._format_node(node.body, depth + 2))
            return "\n".join(lines)
        elif isinstance(node, Block):
            lines = [f"{indent}Block (L{node.line})"]
            for stmt in node.statements:
                lines.append(self._format_node(stmt, depth + 1))
            return "\n".join(lines)
        elif isinstance(node, ExprStmt):
            return f"{indent}ExprStmt (L{node.line}):\n" + self._format_node(node.expr, depth + 1)
        elif isinstance(node, IfStmt):
            lines = [f"{indent}IfStmt (L{node.line}):"]
            lines.append(f"{indent}  Condition:")
            lines.append(self._format_node(node.cond, depth + 2))
            lines.append(f"{indent}  Then:")
            lines.append(self._format_node(node.then_branch, depth + 2))
            if node.else_branch:
                lines.append(f"{indent}  Else:")
                lines.append(self._format_node(node.else_branch, depth + 2))
            return "\n".join(lines)
        elif isinstance(node, WhileStmt):
            lines = [f"{indent}WhileStmt (L{node.line}):"]
            lines.append(f"{indent}  Condition:")
            lines.append(self._format_node(node.cond, depth + 2))
            lines.append(f"{indent}  Body:")
            lines.append(self._format_node(node.body, depth + 2))
            return "\n".join(lines)
        elif isinstance(node, ForStmt):
            lines = [f"{indent}ForStmt (L{node.line}):"]
            if node.init:
                lines.append(f"{indent}  Init:")
                lines.append(self._format_node(node.init, depth + 2))
            if node.cond:
                lines.append(f"{indent}  Cond:")
                lines.append(self._format_node(node.cond, depth + 2))
            if node.step:
                lines.append(f"{indent}  Step:")
                lines.append(self._format_node(node.step, depth + 2))
            lines.append(f"{indent}  Body:")
            lines.append(self._format_node(node.body, depth + 2))
            return "\n".join(lines)
        elif isinstance(node, ReturnStmt):
            if node.expr:
                return f"{indent}ReturnStmt (L{node.line}):\n" + self._format_node(node.expr, depth + 1)
            return f"{indent}ReturnStmt (L{node.line})"
        elif isinstance(node, Literal):
            return f"{indent}Literal({node.lit_type}: {node.value!r}) (L{node.line})"
        elif isinstance(node, VarExpr):
            return f"{indent}VarExpr({node.name}) (L{node.line})"
        elif isinstance(node, ArrayAccessExpr):
            lines = [f"{indent}ArrayAccessExpr (L{node.line}):"]
            lines.append(f"{indent}  Target:")
            lines.append(self._format_node(node.target, depth + 2))
            lines.append(f"{indent}  Indices:")
            for idx in node.indices:
                lines.append(self._format_node(idx, depth + 2))
            return "\n".join(lines)
        elif isinstance(node, FieldAccessExpr):
            lines = [f"{indent}FieldAccessExpr(.{node.field}) (L{node.line}):"]
            lines.append(self._format_node(node.target, depth + 1))
            return "\n".join(lines)
        elif isinstance(node, CallExpr):
            lines = [f"{indent}CallExpr: {node.func_name}() (L{node.line})"]
            if node.args:
                lines.append(f"{indent}  Args:")
                for arg in node.args:
                    lines.append(self._format_node(arg, depth + 2))
            return "\n".join(lines)
        elif isinstance(node, UnaryExpr):
            lines = [f"{indent}UnaryExpr: {node.op} (L{node.line})"]
            lines.append(self._format_node(node.operand, depth + 1))
            return "\n".join(lines)
        elif isinstance(node, BinaryExpr):
            lines = [f"{indent}BinaryExpr: {node.op} (L{node.line})"]
            lines.append(f"{indent}  Left:")
            lines.append(self._format_node(node.left, depth + 2))
            lines.append(f"{indent}  Right:")
            lines.append(self._format_node(node.right, depth + 2))
            return "\n".join(lines)
        elif isinstance(node, AssignExpr):
            lines = [f"{indent}AssignExpr '=' (L{node.line}):"]
            lines.append(f"{indent}  Target:")
            lines.append(self._format_node(node.target, depth + 2))
            lines.append(f"{indent}  Value:")
            lines.append(self._format_node(node.value, depth + 2))
            return "\n".join(lines)
        return f"{indent}{type(node).__name__}({node})"
