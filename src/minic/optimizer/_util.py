"""Shared helpers for the optimization passes.

Everything in here is deliberately conservative: when a fact cannot be proven
cheaply, the helper reports the pessimistic answer so that a transformation
built on top of it stays sound.  MiniC has no pointers and no dynamic memory,
so two *named* locals (or two temporaries) can never alias -- that is the single
invariant every pass leans on.
"""
from typing import Optional, Iterable, List, Set

from ..ir.tac import (
    Opcode, TACInstruction, TACFunction, TACProgram,
    Operand, Temp, Var, Constant, Label,
)

# --- Opcode groups -----------------------------------------------------------

BINARY_ARITH = {Opcode.ADD, Opcode.SUB, Opcode.MUL, Opcode.DIV, Opcode.MOD}
RELATIONAL = {Opcode.EQ, Opcode.NE, Opcode.LT, Opcode.LE, Opcode.GT, Opcode.GE}
BINARY_LOGIC = {Opcode.LOGIC_AND, Opcode.LOGIC_OR}
BINARY_OPS = BINARY_ARITH | RELATIONAL | BINARY_LOGIC
UNARY_OPS = {Opcode.NEG, Opcode.LOGIC_NOT}

COMMUTATIVE = {Opcode.ADD, Opcode.MUL, Opcode.EQ, Opcode.NE,
               Opcode.LOGIC_AND, Opcode.LOGIC_OR}

# Opcodes that compute a fresh value into ``dst`` (pure -- no observable effect
# beyond defining ``dst``).
VALUE_PRODUCING = (
    BINARY_OPS | UNARY_OPS
    | {Opcode.ASSIGN, Opcode.LOAD_ARR_1D, Opcode.LOAD_ARR_2D, Opcode.GET_FIELD}
)

# Opcodes that must never be deleted even when their ``dst`` looks unused.
SIDE_EFFECTING = {
    Opcode.CALL, Opcode.RETURN, Opcode.PARAM,
    Opcode.STORE_ARR_1D, Opcode.STORE_ARR_2D, Opcode.SET_FIELD,
    Opcode.JUMP, Opcode.JUMP_IF_TRUE, Opcode.JUMP_IF_FALSE, Opcode.LABEL,
    Opcode.ALLOC_LOCAL, Opcode.COMMENT,
}


# --- Operand helpers -------------------------------------------------------- -

def op_name(operand: object) -> Optional[str]:
    """Return the symbolic name of a Var/Temp operand, else ``None``."""
    if isinstance(operand, (Var, Temp)):
        return str(operand)
    return None


def is_int_const(operand: object) -> bool:
    return (isinstance(operand, Constant)
            and operand.type_str in ("int", "char")
            and isinstance(operand.value, bool) is False
            and isinstance(operand.value, int))


def const_int_value(operand: object) -> Optional[int]:
    if is_int_const(operand):
        return int(operand.value)
    return None


def value_operand_slots(inst: TACInstruction) -> List[str]:
    """Names of the attributes of ``inst`` that hold *rvalue* operands.

    Excludes label targets, the array/struct base of stores, struct field
    names and call metadata -- i.e. everything that must not be rewritten as if
    it were an ordinary value.
    """
    op = inst.opcode
    if op == Opcode.ASSIGN:
        return ["src1"]
    if op in BINARY_OPS:
        return ["src1", "src2"]
    if op in UNARY_OPS:
        return ["src1"]
    if op in (Opcode.JUMP_IF_TRUE, Opcode.JUMP_IF_FALSE):
        return ["src1"]
    if op == Opcode.RETURN:
        return ["src1"]
    if op == Opcode.PARAM:
        return ["src1"]
    if op == Opcode.LOAD_ARR_1D:
        return ["src2"]
    if op == Opcode.LOAD_ARR_2D:
        return ["src2", "src3"]
    if op == Opcode.STORE_ARR_1D:
        return ["src1", "src2"]
    if op == Opcode.STORE_ARR_2D:
        return ["src1", "src2", "src3"]
    if op == Opcode.SET_FIELD:
        return ["src2"]
    return []


def defined_name(inst: TACInstruction) -> Optional[str]:
    """Name that ``inst`` fully (re)defines, or ``None``.

    Stores / field-writes are *not* reported here: they mutate an aggregate in
    place and are handled as a use+partial-def by the callers that care.
    """
    if inst.opcode in VALUE_PRODUCING:
        return op_name(inst.dst)
    if inst.opcode == Opcode.CALL:
        return op_name(inst.dst)
    return None


def used_names(inst: TACInstruction) -> Set[str]:
    names: Set[str] = set()
    for slot in value_operand_slots(inst):
        n = op_name(getattr(inst, slot))
        if n:
            names.add(n)
    op = inst.opcode
    # The array/struct base of a load is a use ...
    if op in (Opcode.LOAD_ARR_1D, Opcode.LOAD_ARR_2D, Opcode.GET_FIELD):
        n = op_name(inst.src1)
        if n:
            names.add(n)
    # ... and the base of a store is both read and (partially) written, so we
    # keep it live by treating it purely as a use.
    if op in (Opcode.STORE_ARR_1D, Opcode.STORE_ARR_2D, Opcode.SET_FIELD):
        n = op_name(inst.dst)
        if n:
            names.add(n)
    return names


def global_names(prog: Optional[TACProgram]) -> Set[str]:
    if prog is None:
        return set()
    return {g[0] for g in prog.global_vars}


def is_temp_name(name: Optional[str]) -> bool:
    return bool(name) and name[0] == "t" and name[1:].isdigit()


def wrap32(value: int) -> int:
    """Coerce a Python int to a 32-bit two's-complement ``int`` (C semantics)."""
    value &= 0xFFFFFFFF
    if value >= 0x80000000:
        value -= 0x100000000
    return value


def c_div(a: int, b: int) -> int:
    """Integer division truncating toward zero, matching C99."""
    q = abs(a) // abs(b)
    return -q if (a < 0) != (b < 0) else q


def c_mod(a: int, b: int) -> int:
    return a - c_div(a, b) * b


def fold_binary(opcode: Opcode, a: int, b: int) -> Optional[int]:
    """Evaluate an integer binary op with C-int semantics. ``None`` if unsafe."""
    if opcode == Opcode.ADD:
        return wrap32(a + b)
    if opcode == Opcode.SUB:
        return wrap32(a - b)
    if opcode == Opcode.MUL:
        return wrap32(a * b)
    if opcode == Opcode.DIV:
        return wrap32(c_div(a, b)) if b != 0 else None
    if opcode == Opcode.MOD:
        return wrap32(c_mod(a, b)) if b != 0 else None
    if opcode == Opcode.EQ:
        return 1 if a == b else 0
    if opcode == Opcode.NE:
        return 1 if a != b else 0
    if opcode == Opcode.LT:
        return 1 if a < b else 0
    if opcode == Opcode.LE:
        return 1 if a <= b else 0
    if opcode == Opcode.GT:
        return 1 if a > b else 0
    if opcode == Opcode.GE:
        return 1 if a >= b else 0
    if opcode == Opcode.LOGIC_AND:
        return 1 if (a != 0 and b != 0) else 0
    if opcode == Opcode.LOGIC_OR:
        return 1 if (a != 0 or b != 0) else 0
    return None


def fold_unary(opcode: Opcode, a: int) -> Optional[int]:
    if opcode == Opcode.NEG:
        return wrap32(-a)
    if opcode == Opcode.LOGIC_NOT:
        return 1 if a == 0 else 0
    return None


def int_const(value: int) -> Constant:
    return Constant(value=wrap32(int(value)), type_str="int")


def iter_all_instructions(func: TACFunction) -> Iterable[TACInstruction]:
    return list(func.instructions)
