from dataclasses import dataclass, field
from typing import List, Optional, Any, Union


@dataclass
class ASTNode:
    line: int = 0
    col: int = 0


@dataclass
class TypeSpec(ASTNode):
    name: str = ""                # 'int', 'float', 'char', or struct identifier
    is_struct: bool = False       # True if it's a struct type

    def __str__(self) -> str:
        return f"struct {self.name}" if self.is_struct else self.name


@dataclass
class ArraySuffix(ASTNode):
    dim1: int = 0
    dim2: Optional[int] = None

    @property
    def is_2d(self) -> bool:
        return self.dim2 is not None

    def __str__(self) -> str:
        if self.is_2d:
            return f"[{self.dim1}][{self.dim2}]"
        return f"[{self.dim1}]"


@dataclass
class FieldDecl(ASTNode):
    type_spec: TypeSpec = field(default_factory=TypeSpec)
    name: str = ""
    array_suffix: Optional[ArraySuffix] = None


@dataclass
class StructDecl(ASTNode):
    name: str = ""
    fields: List[FieldDecl] = field(default_factory=list)


@dataclass
class VarDecl(ASTNode):
    type_spec: TypeSpec = field(default_factory=TypeSpec)
    name: str = ""
    array_suffix: Optional[ArraySuffix] = None
    init_expr: Optional[ASTNode] = None


@dataclass
class Param(ASTNode):
    type_spec: TypeSpec = field(default_factory=TypeSpec)
    name: str = ""
    array_suffix: Optional[ArraySuffix] = None


@dataclass
class Block(ASTNode):
    statements: List[ASTNode] = field(default_factory=list)


@dataclass
class FuncDecl(ASTNode):
    return_type: TypeSpec = field(default_factory=TypeSpec)
    name: str = ""
    params: List[Param] = field(default_factory=list)
    body: Block = field(default_factory=Block)


@dataclass
class ExprStmt(ASTNode):
    expr: ASTNode = field(default_factory=ASTNode)


@dataclass
class IfStmt(ASTNode):
    cond: ASTNode = field(default_factory=ASTNode)
    then_branch: ASTNode = field(default_factory=ASTNode)
    else_branch: Optional[ASTNode] = None


@dataclass
class WhileStmt(ASTNode):
    cond: ASTNode = field(default_factory=ASTNode)
    body: ASTNode = field(default_factory=ASTNode)


@dataclass
class ForStmt(ASTNode):
    init: Optional[ASTNode] = None       # VarDecl or ExprStmt or None
    cond: Optional[ASTNode] = None       # Expr or None
    step: Optional[ASTNode] = None       # Expr or None
    body: ASTNode = field(default_factory=ASTNode)


@dataclass
class ReturnStmt(ASTNode):
    expr: Optional[ASTNode] = None


# --- Expressions ---

@dataclass
class Literal(ASTNode):
    value: Any = None
    lit_type: str = "int"                 # 'int', 'float', 'char', 'string'


@dataclass
class VarExpr(ASTNode):
    name: str = ""


@dataclass
class ArrayAccessExpr(ASTNode):
    target: ASTNode = field(default_factory=ASTNode)
    indices: List[ASTNode] = field(default_factory=list)   # 1 or 2 expressions


@dataclass
class FieldAccessExpr(ASTNode):
    target: ASTNode = field(default_factory=ASTNode)
    field: str = ""


@dataclass
class CallExpr(ASTNode):
    func_name: str = ""
    args: List[ASTNode] = field(default_factory=list)


@dataclass
class UnaryExpr(ASTNode):
    op: str = ""                          # '-', '!'
    operand: ASTNode = field(default_factory=ASTNode)


@dataclass
class BinaryExpr(ASTNode):
    op: str = ""                          # '+', '-', '*', '/', '%', '==', '!=', '<', '<=', '>', '>=', '&&', '||'
    left: ASTNode = field(default_factory=ASTNode)
    right: ASTNode = field(default_factory=ASTNode)


@dataclass
class AssignExpr(ASTNode):
    target: ASTNode = field(default_factory=ASTNode)
    value: ASTNode = field(default_factory=ASTNode)


@dataclass
class Program(ASTNode):
    declarations: List[ASTNode] = field(default_factory=list)
