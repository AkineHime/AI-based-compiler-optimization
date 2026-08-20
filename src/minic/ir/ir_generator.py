from typing import List, Dict, Optional, Tuple, Any, Union
from ..frontend.ast_nodes import (
    Program, ASTNode, StructDecl, FuncDecl, VarDecl, FieldDecl,
    Param, Block, ExprStmt, IfStmt, WhileStmt, ForStmt, ReturnStmt,
    Literal, VarExpr, ArrayAccessExpr, FieldAccessExpr, CallExpr,
    UnaryExpr, BinaryExpr, AssignExpr, TypeSpec, ArraySuffix
)
from .tac import (
    Opcode, Operand, Temp, Var, Constant, Label,
    TACInstruction, TACFunction, TACProgram
)


class IRGenerator:
    """Lowers a validated MiniC AST into Three-Address Code (TAC)."""

    def __init__(self):
        self.temp_counter: int = 0
        self.label_counter: int = 0
        self.current_func: Optional[TACFunction] = None
        self.struct_defs: Dict[str, Dict[str, str]] = {}

    def new_temp(self, type_str: str = "int") -> Temp:
        t = Temp(id=self.temp_counter, type_str=type_str)
        self.temp_counter += 1
        if self.current_func is not None:
            self.current_func.local_types[str(t)] = type_str
        return t

    def new_label(self, prefix: str = "L") -> Label:
        lbl = Label(name=f"{prefix}{self.label_counter}")
        self.label_counter += 1
        return lbl

    def emit(self, opcode: Opcode, dst: Optional[Operand] = None,
             src1: Optional[Any] = None, src2: Optional[Any] = None,
             src3: Optional[Any] = None, annotation: str = "") -> TACInstruction:
        inst = TACInstruction(opcode=opcode, dst=dst, src1=src1, src2=src2, src3=src3, annotation=annotation)
        if self.current_func is not None:
            self.current_func.instructions.append(inst)
        return inst

    def generate(self, program: Program) -> TACProgram:
        """Lower entire MiniC Program to TACProgram."""
        tac_prog = TACProgram()

        # Step 1: Collect struct definitions
        for decl in program.declarations:
            if isinstance(decl, StructDecl):
                field_dict: Dict[str, str] = {}
                for f in decl.fields:
                    f_type = self._type_to_str(f.type_spec, f.array_suffix)
                    field_dict[f.name] = f_type
                self.struct_defs[decl.name] = field_dict
                tac_prog.structs[decl.name] = field_dict

        # Step 2: Global variables and functions
        for decl in program.declarations:
            if isinstance(decl, VarDecl):
                type_str = self._type_to_str(decl.type_spec, decl.array_suffix)
                init_val = decl.init_expr.value if isinstance(decl.init_expr, Literal) else None
                tac_prog.global_vars.append((decl.name, type_str, init_val))
            elif isinstance(decl, FuncDecl):
                func_tac = self._lower_function(decl)
                tac_prog.functions.append(func_tac)

        return tac_prog

    def _type_to_str(self, type_spec: TypeSpec, suffix: Optional[ArraySuffix]) -> str:
        base = f"struct {type_spec.name}" if type_spec.is_struct else type_spec.name
        if suffix:
            if suffix.is_2d:
                return f"{base}[{suffix.dim1}][{suffix.dim2}]"
            return f"{base}[{suffix.dim1}]"
        return base

    def _lower_function(self, func: FuncDecl) -> TACFunction:
        ret_type_str = self._type_to_str(func.return_type, None)
        params_list = [(p.name, self._type_to_str(p.type_spec, p.array_suffix)) for p in func.params]

        tac_func = TACFunction(name=func.name, return_type=ret_type_str, params=params_list)
        self.current_func = tac_func

        # Register parameters in local types
        for p_name, p_type in params_list:
            tac_func.local_types[p_name] = p_type

        # Lower body
        self._lower_block(func.body)

        # Ensure implicit return if none at end
        if not tac_func.instructions or tac_func.instructions[-1].opcode != Opcode.RETURN:
            if ret_type_str == "void":
                self.emit(Opcode.RETURN)
            else:
                self.emit(Opcode.RETURN, src1=Constant(0, "int"))

        self.current_func = None
        return tac_func

    def _lower_block(self, block: Block) -> None:
        for stmt in block.statements:
            self._lower_stmt(stmt)

    def _lower_stmt(self, stmt: ASTNode) -> None:
        if isinstance(stmt, VarDecl):
            type_str = self._type_to_str(stmt.type_spec, stmt.array_suffix)
            if self.current_func:
                self.current_func.local_types[stmt.name] = type_str
            self.emit(Opcode.ALLOC_LOCAL, dst=Var(stmt.name, type_str), src1=type_str)

            if stmt.init_expr is not None:
                val = self._lower_expr(stmt.init_expr)
                self.emit(Opcode.ASSIGN, dst=Var(stmt.name, type_str), src1=val)

        elif isinstance(stmt, ExprStmt):
            self._lower_expr(stmt.expr)

        elif isinstance(stmt, Block):
            self._lower_block(stmt)

        elif isinstance(stmt, IfStmt):
            self._lower_if(stmt)

        elif isinstance(stmt, WhileStmt):
            self._lower_while(stmt)

        elif isinstance(stmt, ForStmt):
            self._lower_for(stmt)

        elif isinstance(stmt, ReturnStmt):
            if stmt.expr is not None:
                val = self._lower_expr(stmt.expr)
                self.emit(Opcode.RETURN, src1=val)
            else:
                self.emit(Opcode.RETURN)

    def _lower_if(self, stmt: IfStmt) -> None:
        l_else = self.new_label("L_else")
        l_end = self.new_label("L_endif")

        cond_val = self._lower_expr(stmt.cond)
        self.emit(Opcode.JUMP_IF_FALSE, dst=l_else if stmt.else_branch else l_end, src1=cond_val)

        self._lower_stmt(stmt.then_branch)

        if stmt.else_branch:
            self.emit(Opcode.JUMP, dst=l_end)
            self.emit(Opcode.LABEL, dst=l_else)
            self._lower_stmt(stmt.else_branch)
            self.emit(Opcode.LABEL, dst=l_end)
        else:
            self.emit(Opcode.LABEL, dst=l_end)

    def _lower_while(self, stmt: WhileStmt) -> None:
        l_start = self.new_label("L_while_start")
        l_end = self.new_label("L_while_end")

        self.emit(Opcode.LABEL, dst=l_start)
        cond_val = self._lower_expr(stmt.cond)
        self.emit(Opcode.JUMP_IF_FALSE, dst=l_end, src1=cond_val)

        self._lower_stmt(stmt.body)
        self.emit(Opcode.JUMP, dst=l_start)
        self.emit(Opcode.LABEL, dst=l_end)

    def _lower_for(self, stmt: ForStmt) -> None:
        l_start = self.new_label("L_for_start")
        l_end = self.new_label("L_for_end")

        if stmt.init:
            self._lower_stmt(stmt.init)

        self.emit(Opcode.LABEL, dst=l_start)

        if stmt.cond:
            cond_val = self._lower_expr(stmt.cond)
            self.emit(Opcode.JUMP_IF_FALSE, dst=l_end, src1=cond_val)

        self._lower_stmt(stmt.body)

        if stmt.step:
            self._lower_expr(stmt.step)

        self.emit(Opcode.JUMP, dst=l_start)
        self.emit(Opcode.LABEL, dst=l_end)

    # --- Expression Lowering ---

    def _lower_expr(self, expr: ASTNode) -> Operand:
        if isinstance(expr, Literal):
            return Constant(value=expr.value, type_str=expr.lit_type)

        elif isinstance(expr, VarExpr):
            var_type = self.current_func.local_types.get(expr.name, "int") if self.current_func else "int"
            return Var(name=expr.name, type_str=var_type)

        elif isinstance(expr, AssignExpr):
            rhs_val = self._lower_expr(expr.value)

            if isinstance(expr.target, VarExpr):
                var_type = self.current_func.local_types.get(expr.target.name, "int") if self.current_func else "int"
                dst_var = Var(name=expr.target.name, type_str=var_type)
                self.emit(Opcode.ASSIGN, dst=dst_var, src1=rhs_val)
                return dst_var

            elif isinstance(expr.target, ArrayAccessExpr):
                arr_operand = self._lower_expr(expr.target.target)
                if len(expr.target.indices) == 1:
                    idx = self._lower_expr(expr.target.indices[0])
                    self.emit(Opcode.STORE_ARR_1D, dst=arr_operand, src1=idx, src2=rhs_val)
                elif len(expr.target.indices) == 2:
                    idx1 = self._lower_expr(expr.target.indices[0])
                    idx2 = self._lower_expr(expr.target.indices[1])
                    self.emit(Opcode.STORE_ARR_2D, dst=arr_operand, src1=idx1, src2=idx2, src3=rhs_val)
                return rhs_val

            elif isinstance(expr.target, FieldAccessExpr):
                struct_operand = self._lower_expr(expr.target.target)
                self.emit(Opcode.SET_FIELD, dst=struct_operand, src1=expr.target.field, src2=rhs_val)
                return rhs_val

        elif isinstance(expr, ArrayAccessExpr):
            arr_operand = self._lower_expr(expr.target)
            t = self.new_temp()
            if len(expr.indices) == 1:
                idx = self._lower_expr(expr.indices[0])
                self.emit(Opcode.LOAD_ARR_1D, dst=t, src1=arr_operand, src2=idx)
            elif len(expr.indices) == 2:
                idx1 = self._lower_expr(expr.indices[0])
                idx2 = self._lower_expr(expr.indices[1])
                self.emit(Opcode.LOAD_ARR_2D, dst=t, src1=arr_operand, src2=idx1, src3=idx2)
            return t

        elif isinstance(expr, FieldAccessExpr):
            struct_operand = self._lower_expr(expr.target)
            t = self.new_temp()
            self.emit(Opcode.GET_FIELD, dst=t, src1=struct_operand, src2=expr.field)
            return t

        elif isinstance(expr, CallExpr):
            # Evaluate arguments
            arg_operands: List[Operand] = [self._lower_expr(arg) for arg in expr.args]
            for arg_op in arg_operands:
                self.emit(Opcode.PARAM, src1=arg_op)

            t = self.new_temp()
            self.emit(Opcode.CALL, dst=t, src1=expr.func_name, src2=len(arg_operands))
            return t

        elif isinstance(expr, UnaryExpr):
            operand_val = self._lower_expr(expr.operand)
            t = self.new_temp()
            if expr.op == '-':
                self.emit(Opcode.NEG, dst=t, src1=operand_val)
            elif expr.op == '!':
                self.emit(Opcode.LOGIC_NOT, dst=t, src1=operand_val)
            return t

        elif isinstance(expr, BinaryExpr):
            # Short-circuit logic for && and ||
            if expr.op == '&&':
                return self._lower_short_circuit_and(expr)
            elif expr.op == '||':
                return self._lower_short_circuit_or(expr)

            left_val = self._lower_expr(expr.left)
            right_val = self._lower_expr(expr.right)
            t = self.new_temp()

            op_map = {
                '+': Opcode.ADD, '-': Opcode.SUB, '*': Opcode.MUL, '/': Opcode.DIV, '%': Opcode.MOD,
                '==': Opcode.EQ, '!=': Opcode.NE, '<': Opcode.LT, '<=': Opcode.LE, '>': Opcode.GT, '>=': Opcode.GE,
            }
            if expr.op in op_map:
                self.emit(op_map[expr.op], dst=t, src1=left_val, src2=right_val)
            return t

        return Constant(0, "int")

    def _lower_short_circuit_and(self, expr: BinaryExpr) -> Temp:
        t = self.new_temp()
        l_false = self.new_label("L_and_false")
        l_end = self.new_label("L_and_end")

        left_val = self._lower_expr(expr.left)
        self.emit(Opcode.JUMP_IF_FALSE, dst=l_false, src1=left_val)

        right_val = self._lower_expr(expr.right)
        self.emit(Opcode.JUMP_IF_FALSE, dst=l_false, src1=right_val)

        self.emit(Opcode.ASSIGN, dst=t, src1=Constant(1, "int"))
        self.emit(Opcode.JUMP, dst=l_end)

        self.emit(Opcode.LABEL, dst=l_false)
        self.emit(Opcode.ASSIGN, dst=t, src1=Constant(0, "int"))

        self.emit(Opcode.LABEL, dst=l_end)
        return t

    def _lower_short_circuit_or(self, expr: BinaryExpr) -> Temp:
        t = self.new_temp()
        l_true = self.new_label("L_or_true")
        l_end = self.new_label("L_or_end")

        left_val = self._lower_expr(expr.left)
        self.emit(Opcode.JUMP_IF_TRUE, dst=l_true, src1=left_val)

        right_val = self._lower_expr(expr.right)
        self.emit(Opcode.JUMP_IF_TRUE, dst=l_true, src1=right_val)

        self.emit(Opcode.ASSIGN, dst=t, src1=Constant(0, "int"))
        self.emit(Opcode.JUMP, dst=l_end)

        self.emit(Opcode.LABEL, dst=l_true)
        self.emit(Opcode.ASSIGN, dst=t, src1=Constant(1, "int"))

        self.emit(Opcode.LABEL, dst=l_end)
        return t
