from typing import Dict, List, Optional, Tuple, Set, Any
from dataclasses import dataclass
from .ast_nodes import (
    Program, ASTNode, StructDecl, FuncDecl, VarDecl, FieldDecl,
    Param, Block, ExprStmt, IfStmt, WhileStmt, ForStmt, ReturnStmt,
    Literal, VarExpr, ArrayAccessExpr, FieldAccessExpr, CallExpr,
    UnaryExpr, BinaryExpr, AssignExpr, TypeSpec, ArraySuffix
)
from .error_handler import SemanticError


@dataclass
class TypeInfo:
    base_type: str              # 'int', 'float', 'char', or struct name
    is_struct: bool = False
    dim1: Optional[int] = None  # None if not array
    dim2: Optional[int] = None  # None if 1D or not array

    @property
    def is_array(self) -> bool:
        return self.dim1 is not None

    @property
    def is_2d_array(self) -> bool:
        return self.dim1 is not None and self.dim2 is not None

    def __str__(self) -> str:
        s = f"struct {self.base_type}" if self.is_struct else self.base_type
        if self.is_2d_array:
            s += f"[{self.dim1}][{self.dim2}]"
        elif self.is_array:
            s += f"[{self.dim1}]"
        return s

    def is_compatible_with(self, other: 'TypeInfo') -> bool:
        """Check strict type compatibility per MiniC specification."""
        if self.is_struct != other.is_struct:
            return False
        if self.is_struct and self.base_type != other.base_type:
            return False

        # Numeric compatibility
        if not self.is_struct and not self.is_array and not other.is_array:
            if self.base_type in ('int', 'float', 'char') and other.base_type in ('int', 'float', 'char'):
                return True

        if self.base_type != other.base_type:
            return False
        if self.dim1 != other.dim1 or self.dim2 != other.dim2:
            return False

        return True


@dataclass
class StructInfo:
    name: str
    fields: Dict[str, TypeInfo]
    field_order: List[str]


@dataclass
class FuncInfo:
    name: str
    return_type: TypeInfo
    params: List[Tuple[str, TypeInfo]]


class SymbolTable:
    def __init__(self, parent: Optional['SymbolTable'] = None):
        self.parent: Optional['SymbolTable'] = parent
        self.symbols: Dict[str, TypeInfo] = {}

    def define(self, name: str, type_info: TypeInfo) -> bool:
        """Define a symbol in current scope. Returns False if already defined in THIS scope."""
        if name in self.symbols:
            return False
        self.symbols[name] = type_info
        return True

    def lookup(self, name: str) -> Optional[TypeInfo]:
        """Look up symbol in current and enclosing scopes."""
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        return None


class SemanticAnalyzer:
    """MiniC Semantic Analyzer and Type Checker."""

    def __init__(self, source: str = ""):
        self.source: str = source
        self.structs: Dict[str, StructInfo] = {}
        self.functions: Dict[str, FuncInfo] = {}
        self.global_symtab: SymbolTable = SymbolTable()
        self.current_symtab: SymbolTable = self.global_symtab
        self.current_func: Optional[FuncInfo] = None

    def analyze(self, program: Program) -> None:
        """Run all semantic checks on the program AST."""
        # First pass: collect struct declarations and function signatures
        for decl in program.declarations:
            if isinstance(decl, StructDecl):
                self._declare_struct(decl)
            elif isinstance(decl, FuncDecl):
                self._declare_func_signature(decl)

        # Check for recursive struct definitions
        self._check_struct_recursion()

        # Second pass: check function bodies and global variables
        for decl in program.declarations:
            if isinstance(decl, VarDecl):
                self._check_var_decl(decl, is_global=True)
            elif isinstance(decl, FuncDecl):
                self._check_func_body(decl)

    def _make_type_info(self, type_spec: TypeSpec, array_suffix: Optional[ArraySuffix]) -> TypeInfo:
        dim1 = array_suffix.dim1 if array_suffix else None
        dim2 = array_suffix.dim2 if array_suffix else None
        return TypeInfo(
            base_type=type_spec.name,
            is_struct=type_spec.is_struct,
            dim1=dim1,
            dim2=dim2
        )

    def _declare_struct(self, decl: StructDecl) -> None:
        if decl.name in self.structs:
            raise SemanticError(f"Duplicate declaration of struct {decl.name!r}", decl.line, decl.col, self.source)

        fields: Dict[str, TypeInfo] = {}
        field_order: List[str] = []

        for field in decl.fields:
            if field.name in fields:
                raise SemanticError(f"Duplicate field {field.name!r} in struct {decl.name!r}", field.line, field.col, self.source)
            type_info = self._make_type_info(field.type_spec, field.array_suffix)
            fields[field.name] = type_info
            field_order.append(field.name)

        self.structs[decl.name] = StructInfo(name=decl.name, fields=fields, field_order=field_order)

    def _check_struct_recursion(self) -> None:
        """Ensure no struct contains itself directly or indirectly."""
        for struct_name, struct_info in self.structs.items():
            visited: Set[str] = set()
            stack: List[str] = [struct_name]

            while stack:
                curr = stack.pop()
                if curr in visited:
                    continue
                visited.add(curr)

                if curr in self.structs:
                    for field_type in self.structs[curr].fields.values():
                        if field_type.is_struct:
                            if field_type.base_type == struct_name:
                                raise SemanticError(
                                    f"Recursive struct definition detected: {struct_name!r} contains {field_type.base_type!r}",
                                    0, 0, self.source
                                )
                            stack.append(field_type.base_type)

    def _declare_func_signature(self, decl: FuncDecl) -> None:
        if decl.name in self.functions:
            raise SemanticError(f"Duplicate function definition {decl.name!r}", decl.line, decl.col, self.source)

        ret_type = self._make_type_info(decl.return_type, None)
        params: List[Tuple[str, TypeInfo]] = []
        param_names: Set[str] = set()

        for param in decl.params:
            if param.name in param_names:
                raise SemanticError(f"Duplicate parameter name {param.name!r} in function {decl.name!r}", param.line, param.col, self.source)
            param_names.add(param.name)
            p_type = self._make_type_info(param.type_spec, param.array_suffix)
            self._validate_type(p_type, param.line, param.col)
            params.append((param.name, p_type))

        self._validate_type(ret_type, decl.line, decl.col)
        self.functions[decl.name] = FuncInfo(name=decl.name, return_type=ret_type, params=params)

    def _validate_type(self, type_info: TypeInfo, line: int, col: int) -> None:
        if type_info.is_struct:
            if type_info.base_type not in self.structs:
                raise SemanticError(f"Unknown struct type {type_info.base_type!r}", line, col, self.source)
        else:
            if type_info.base_type not in ('int', 'float', 'char', 'void'):
                raise SemanticError(f"Unknown type specifier {type_info.base_type!r}", line, col, self.source)

    def _check_func_body(self, decl: FuncDecl) -> None:
        func_info = self.functions[decl.name]
        self.current_func = func_info

        # Create function scope
        func_symtab = SymbolTable(parent=self.global_symtab)
        self.current_symtab = func_symtab

        # Define parameters in scope
        for p_name, p_type in func_info.params:
            func_symtab.define(p_name, p_type)

        self._check_block(decl.body, is_func_root=True)

        self.current_symtab = self.global_symtab
        self.current_func = None

    def _check_block(self, block: Block, is_func_root: bool = False) -> None:
        if not is_func_root:
            block_symtab = SymbolTable(parent=self.current_symtab)
            self.current_symtab = block_symtab

        for stmt in block.statements:
            self._check_stmt(stmt)

        if not is_func_root and self.current_symtab.parent is not None:
            self.current_symtab = self.current_symtab.parent

    def _check_stmt(self, stmt: ASTNode) -> None:
        if isinstance(stmt, VarDecl):
            self._check_var_decl(stmt, is_global=False)
        elif isinstance(stmt, ExprStmt):
            self._check_expr(stmt.expr)
        elif isinstance(stmt, Block):
            self._check_block(stmt)
        elif isinstance(stmt, IfStmt):
            cond_type = self._check_expr(stmt.cond)
            if cond_type.is_array:
                raise SemanticError("Condition expression cannot be an array", stmt.cond.line, stmt.cond.col, self.source)
            self._check_stmt(stmt.then_branch)
            if stmt.else_branch:
                self._check_stmt(stmt.else_branch)
        elif isinstance(stmt, WhileStmt):
            cond_type = self._check_expr(stmt.cond)
            if cond_type.is_array:
                raise SemanticError("Condition expression cannot be an array", stmt.cond.line, stmt.cond.col, self.source)
            self._check_stmt(stmt.body)
        elif isinstance(stmt, ForStmt):
            # For loop creates its own scope for init
            for_symtab = SymbolTable(parent=self.current_symtab)
            self.current_symtab = for_symtab

            if stmt.init:
                if isinstance(stmt.init, VarDecl):
                    self._check_var_decl(stmt.init, is_global=False)
                else:
                    self._check_expr(stmt.init)
            if stmt.cond:
                self._check_expr(stmt.cond)
            if stmt.step:
                self._check_expr(stmt.step)

            self._check_stmt(stmt.body)
            if self.current_symtab.parent is not None:
                self.current_symtab = self.current_symtab.parent
        elif isinstance(stmt, ReturnStmt):
            if stmt.expr:
                expr_type = self._check_expr(stmt.expr)
                if self.current_func and not expr_type.is_compatible_with(self.current_func.return_type):
                    raise SemanticError(
                        f"Return type mismatch: expected {self.current_func.return_type}, got {expr_type}",
                        stmt.line, stmt.col, self.source
                    )
            else:
                if self.current_func and self.current_func.return_type.base_type != "void":
                    raise SemanticError(f"Non-void function {self.current_func.name!r} must return a value", stmt.line, stmt.col, self.source)

    def _check_var_decl(self, decl: VarDecl, is_global: bool = False) -> None:
        type_info = self._make_type_info(decl.type_spec, decl.array_suffix)
        self._validate_type(type_info, decl.line, decl.col)

        if not self.current_symtab.define(decl.name, type_info):
            raise SemanticError(f"Redefinition of variable {decl.name!r}", decl.line, decl.col, self.source)

        if decl.init_expr:
            init_type = self._check_expr(decl.init_expr)
            # Special case for string literal initializing char array
            if type_info.base_type == 'char' and type_info.is_array and not type_info.is_2d_array:
                if isinstance(decl.init_expr, Literal) and decl.init_expr.lit_type == "string":
                    str_len = len(decl.init_expr.value)
                    if type_info.dim1 is not None and type_info.dim1 < str_len + 1:
                        raise SemanticError(
                            f"String literal requires buffer size >= {str_len + 1}, but array size is {type_info.dim1}",
                            decl.line, decl.col, self.source
                        )
                    return

            if not init_type.is_compatible_with(type_info):
                raise SemanticError(
                    f"Type mismatch in initialization of {decl.name!r}: expected {type_info}, got {init_type}",
                    decl.line, decl.col, self.source
                )

    def _check_expr(self, expr: ASTNode) -> TypeInfo:
        if isinstance(expr, Literal):
            if expr.lit_type == "int":
                return TypeInfo(base_type="int")
            elif expr.lit_type == "float":
                return TypeInfo(base_type="float")
            elif expr.lit_type == "char":
                return TypeInfo(base_type="char")
            elif expr.lit_type == "string":
                # String literal has type char[len + 1]
                return TypeInfo(base_type="char", dim1=len(expr.value) + 1)

        elif isinstance(expr, VarExpr):
            type_info = self.current_symtab.lookup(expr.name)
            if not type_info:
                raise SemanticError(f"Undeclared variable {expr.name!r}", expr.line, expr.col, self.source)
            return type_info

        elif isinstance(expr, ArrayAccessExpr):
            target_type = self._check_expr(expr.target)
            if not target_type.is_array:
                raise SemanticError(f"Cannot index non-array type {target_type}", expr.line, expr.col, self.source)

            # Check index types
            for idx in expr.indices:
                idx_type = self._check_expr(idx)
                if idx_type.base_type not in ('int', 'char') or idx_type.is_array:
                    raise SemanticError(f"Array subscript must be an integer, got {idx_type}", idx.line, idx.col, self.source)

            if len(expr.indices) == 1:
                if target_type.is_2d_array:
                    # 1 index on 2D array yields 1D array row
                    return TypeInfo(base_type=target_type.base_type, is_struct=target_type.is_struct, dim1=target_type.dim2)
                else:
                    return TypeInfo(base_type=target_type.base_type, is_struct=target_type.is_struct)
            elif len(expr.indices) == 2:
                if not target_type.is_2d_array:
                    raise SemanticError(f"Cannot use 2 indices on 1D array {target_type}", expr.line, expr.col, self.source)
                return TypeInfo(base_type=target_type.base_type, is_struct=target_type.is_struct)
            else:
                raise SemanticError("MiniC supports up to 2 array dimensions", expr.line, expr.col, self.source)

        elif isinstance(expr, FieldAccessExpr):
            target_type = self._check_expr(expr.target)
            if not target_type.is_struct or target_type.is_array:
                raise SemanticError(f"Member access '.' on non-struct type {target_type}", expr.line, expr.col, self.source)

            struct_info = self.structs.get(target_type.base_type)
            if not struct_info or expr.field not in struct_info.fields:
                raise SemanticError(f"Struct {target_type.base_type!r} has no field {expr.field!r}", expr.line, expr.col, self.source)
            return struct_info.fields[expr.field]

        elif isinstance(expr, CallExpr):
            func_info = self.functions.get(expr.func_name)
            if not func_info:
                raise SemanticError(f"Call to undeclared function {expr.func_name!r}", expr.line, expr.col, self.source)

            if len(expr.args) != len(func_info.params):
                raise SemanticError(
                    f"Function {expr.func_name!r} expects {len(func_info.params)} arguments, got {len(expr.args)}",
                    expr.line, expr.col, self.source
                )

            for arg_expr, (param_name, param_type) in zip(expr.args, func_info.params):
                arg_type = self._check_expr(arg_expr)
                if not arg_type.is_compatible_with(param_type):
                    raise SemanticError(
                        f"Argument type mismatch for parameter {param_name!r} in call to {expr.func_name!r}: expected {param_type}, got {arg_type}",
                        arg_expr.line, arg_expr.col, self.source
                    )

            return func_info.return_type

        elif isinstance(expr, UnaryExpr):
            operand_type = self._check_expr(expr.operand)
            if operand_type.is_array or operand_type.is_struct:
                raise SemanticError(f"Unary operator {expr.op!r} not supported on {operand_type}", expr.line, expr.col, self.source)
            return operand_type

        elif isinstance(expr, BinaryExpr):
            left_type = self._check_expr(expr.left)
            right_type = self._check_expr(expr.right)

            if left_type.is_array or right_type.is_array or left_type.is_struct or right_type.is_struct:
                raise SemanticError(f"Binary operator {expr.op!r} not supported on types {left_type} and {right_type}", expr.line, expr.col, self.source)

            if expr.op in ('==', '!=', '<', '<=', '>', '>=', '&&', '||'):
                return TypeInfo(base_type="int")

            if left_type.base_type == "float" or right_type.base_type == "float":
                return TypeInfo(base_type="float")
            return TypeInfo(base_type="int")

        elif isinstance(expr, AssignExpr):
            # L-Value check
            if not isinstance(expr.target, (VarExpr, ArrayAccessExpr, FieldAccessExpr)):
                raise SemanticError("Invalid l-value on left side of assignment", expr.line, expr.col, self.source)

            target_type = self._check_expr(expr.target)
            value_type = self._check_expr(expr.value)

            if not value_type.is_compatible_with(target_type):
                raise SemanticError(
                    f"Cannot assign {value_type} to variable of type {target_type}",
                    expr.line, expr.col, self.source
                )
            return target_type

        raise SemanticError(f"Unknown expression node {type(expr).__name__}", expr.line, expr.col, self.source)
