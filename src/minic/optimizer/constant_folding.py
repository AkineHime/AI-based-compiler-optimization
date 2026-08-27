import copy
from typing import Dict, List, Optional, Any, Tuple
from ..ir.tac import (
    TACProgram, TACFunction, TACInstruction, Opcode,
    Operand, Temp, Var, Constant, Label
)
from ..ir.cfg import build_cfg_for_function, CFG
from ._util import wrap32, c_div, c_mod


def constant_folding_pass(func: TACFunction) -> TACFunction:
    """Performs constant folding, constant propagation, and branch simplification on a function."""
    changed = True
    max_iterations = 20
    iteration = 0

    optimized_func = copy.deepcopy(func)

    while changed and iteration < max_iterations:
        changed = False
        iteration += 1

        # Step 1: Forward constant propagation and expression evaluation
        new_instructions: List[TACInstruction] = []
        
        # Temp constants map (SSA-like temporaries)
        temp_constants: Dict[str, Constant] = {}
        # Block-local variable constants
        var_constants: Dict[str, Constant] = {}

        for inst in optimized_func.instructions:
            op = inst.opcode

            # Reset local var constants on control flow targets/jumps
            if op in (Opcode.LABEL, Opcode.JUMP, Opcode.JUMP_IF_TRUE, Opcode.JUMP_IF_FALSE, Opcode.CALL):
                var_constants.clear()

            # Substitute operands from known constants
            src1 = _substitute_constant(inst.src1, temp_constants, var_constants)
            src2 = _substitute_constant(inst.src2, temp_constants, var_constants)
            src3 = _substitute_constant(inst.src3, temp_constants, var_constants)

            if src1 != inst.src1 or src2 != inst.src2 or src3 != inst.src3:
                changed = True

            # Evaluate binary operations
            if op in (
                Opcode.ADD, Opcode.SUB, Opcode.MUL, Opcode.DIV, Opcode.MOD,
                Opcode.EQ, Opcode.NE, Opcode.LT, Opcode.LE, Opcode.GT, Opcode.GE,
                Opcode.LOGIC_AND, Opcode.LOGIC_OR
            ):
                if isinstance(src1, Constant) and isinstance(src2, Constant):
                    folded_val, val_type = _evaluate_binary_op(op, src1.value, src2.value, src1.type_str, src2.type_str)
                    if folded_val is not None:
                        c_res = Constant(value=folded_val, type_str=val_type)
                        new_inst = TACInstruction(Opcode.ASSIGN, dst=inst.dst, src1=c_res)
                        new_instructions.append(new_inst)
                        if isinstance(inst.dst, Temp):
                            temp_constants[str(inst.dst)] = c_res
                        elif isinstance(inst.dst, Var):
                            var_constants[inst.dst.name] = c_res
                        changed = True
                        continue

                # Algebraic simplifications
                simplified = _simplify_algebraic(op, inst.dst, src1, src2)
                if simplified is not None:
                    new_instructions.append(simplified)
                    if simplified.opcode == Opcode.ASSIGN and isinstance(simplified.src1, Constant):
                        if isinstance(simplified.dst, Temp):
                            temp_constants[str(simplified.dst)] = simplified.src1
                        elif isinstance(simplified.dst, Var):
                            var_constants[simplified.dst.name] = simplified.src1
                    changed = True
                    continue

            # Evaluate unary operations
            elif op in (Opcode.NEG, Opcode.LOGIC_NOT):
                if isinstance(src1, Constant):
                    folded_val, val_type = _evaluate_unary_op(op, src1.value, src1.type_str)
                    if folded_val is not None:
                        c_res = Constant(value=folded_val, type_str=val_type)
                        new_inst = TACInstruction(Opcode.ASSIGN, dst=inst.dst, src1=c_res)
                        new_instructions.append(new_inst)
                        if isinstance(inst.dst, Temp):
                            temp_constants[str(inst.dst)] = c_res
                        elif isinstance(inst.dst, Var):
                            var_constants[inst.dst.name] = c_res
                        changed = True
                        continue

            # Simplify conditional branches on constant conditions
            elif op == Opcode.JUMP_IF_TRUE:
                if isinstance(src1, Constant):
                    if src1.value != 0:
                        # Always true -> unconditional jump
                        new_instructions.append(TACInstruction(Opcode.JUMP, dst=inst.dst))
                    # If false -> branch never taken, eliminate
                    changed = True
                    continue

            elif op == Opcode.JUMP_IF_FALSE:
                if isinstance(src1, Constant):
                    if src1.value == 0:
                        # Always false -> unconditional jump
                        new_instructions.append(TACInstruction(Opcode.JUMP, dst=inst.dst))
                    # If true -> branch never taken, eliminate
                    changed = True
                    continue

            # Tracking assignments
            elif op == Opcode.ASSIGN:
                if isinstance(inst.dst, Temp):
                    if isinstance(src1, Constant):
                        temp_constants[str(inst.dst)] = src1
                elif isinstance(inst.dst, Var):
                    if isinstance(src1, Constant):
                        var_constants[inst.dst.name] = src1
                    else:
                        var_constants.pop(inst.dst.name, None)

            # Invalidate variable constant if it is mutated in aggregate store or field write
            elif op in (Opcode.STORE_ARR_1D, Opcode.STORE_ARR_2D, Opcode.SET_FIELD):
                if isinstance(inst.dst, Var):
                    var_constants.pop(inst.dst.name, None)

            new_instructions.append(
                TACInstruction(
                    opcode=op, dst=inst.dst, src1=src1, src2=src2, src3=src3, annotation=inst.annotation
                )
            )

        optimized_func.instructions = new_instructions

    return optimized_func


def _substitute_constant(operand: Any, temp_constants: Dict[str, Constant], var_constants: Dict[str, Constant]) -> Any:
    if isinstance(operand, Temp):
        key = str(operand)
        if key in temp_constants:
            return temp_constants[key]
    elif isinstance(operand, Var):
        if operand.name in var_constants:
            return var_constants[operand.name]
    return operand


def _evaluate_binary_op(op: Opcode, v1: Any, v2: Any, t1: str, t2: str) -> Tuple[Optional[Any], str]:
    res_type = "float" if (t1 == "float" or t2 == "float") else "int"
    # Only fold integer arithmetic. Float folding is skipped so the compile-time
    # result can never disagree with the C runtime's rounding.
    if res_type != "int" and op in (
        Opcode.ADD, Opcode.SUB, Opcode.MUL, Opcode.DIV, Opcode.MOD
    ):
        return None, res_type
    try:
        if op == Opcode.ADD:
            val = wrap32(v1 + v2)
        elif op == Opcode.SUB:
            val = wrap32(v1 - v2)
        elif op == Opcode.MUL:
            val = wrap32(v1 * v2)
        elif op == Opcode.DIV:
            if v2 == 0:
                return None, res_type
            val = wrap32(c_div(v1, v2))
        elif op == Opcode.MOD:
            if v2 == 0:
                return None, res_type
            val = wrap32(c_mod(v1, v2))
        elif op == Opcode.EQ:
            val = 1 if v1 == v2 else 0
            res_type = "int"
        elif op == Opcode.NE:
            val = 1 if v1 != v2 else 0
            res_type = "int"
        elif op == Opcode.LT:
            val = 1 if v1 < v2 else 0
            res_type = "int"
        elif op == Opcode.LE:
            val = 1 if v1 <= v2 else 0
            res_type = "int"
        elif op == Opcode.GT:
            val = 1 if v1 > v2 else 0
            res_type = "int"
        elif op == Opcode.GE:
            val = 1 if v1 >= v2 else 0
            res_type = "int"
        elif op == Opcode.LOGIC_AND:
            val = 1 if (v1 != 0 and v2 != 0) else 0
            res_type = "int"
        elif op == Opcode.LOGIC_OR:
            val = 1 if (v1 != 0 or v2 != 0) else 0
            res_type = "int"
        else:
            return None, res_type

        return val, res_type
    except Exception:
        return None, res_type


def _evaluate_unary_op(op: Opcode, v: Any, t: str) -> Tuple[Optional[Any], str]:
    if op == Opcode.NEG:
        if t == "float":
            return None, t
        return wrap32(-v), t
    elif op == Opcode.LOGIC_NOT:
        return (1 if v == 0 else 0), "int"
    return None, t


def _simplify_algebraic(op: Opcode, dst: Optional[Operand], src1: Any, src2: Any) -> Optional[TACInstruction]:
    # Identities like ``x * 0 -> 0`` do not hold for IEEE floats (NaN/inf), so
    # only simplify when every constant operand is an integer.
    for s in (src1, src2):
        if isinstance(s, Constant) and s.type_str not in ("int", "char"):
            return None

    # x + 0 -> x
    if op == Opcode.ADD:
        if isinstance(src2, Constant) and src2.value == 0:
            return TACInstruction(Opcode.ASSIGN, dst=dst, src1=src1)
        if isinstance(src1, Constant) and src1.value == 0:
            return TACInstruction(Opcode.ASSIGN, dst=dst, src1=src2)

    # x - 0 -> x
    elif op == Opcode.SUB:
        if isinstance(src2, Constant) and src2.value == 0:
            return TACInstruction(Opcode.ASSIGN, dst=dst, src1=src1)

    # x * 1 -> x, x * 0 -> 0
    elif op == Opcode.MUL:
        if isinstance(src2, Constant):
            if src2.value == 1:
                return TACInstruction(Opcode.ASSIGN, dst=dst, src1=src1)
            elif src2.value == 0:
                return TACInstruction(Opcode.ASSIGN, dst=dst, src1=Constant(0, "int"))
        if isinstance(src1, Constant):
            if src1.value == 1:
                return TACInstruction(Opcode.ASSIGN, dst=dst, src1=src2)
            elif src1.value == 0:
                return TACInstruction(Opcode.ASSIGN, dst=dst, src1=Constant(0, "int"))

    # x / 1 -> x
    elif op == Opcode.DIV:
        if isinstance(src2, Constant) and src2.value == 1:
            return TACInstruction(Opcode.ASSIGN, dst=dst, src1=src1)

    return None
