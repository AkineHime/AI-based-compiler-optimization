"""Small shared helpers for the optimization passes.

Kept intentionally tiny -- just the bits that more than one pass needs and that
are easy to get subtly wrong (32-bit C integer semantics, the set of global
names a call may clobber).
"""
from typing import Optional

from ..ir.tac import (
    TACProgram, TACInstruction, Opcode, Operand, Temp, Var, Constant,
)

_VALUE_PRODUCING = frozenset({
    Opcode.ASSIGN, Opcode.ADD, Opcode.SUB, Opcode.MUL, Opcode.DIV, Opcode.MOD,
    Opcode.EQ, Opcode.NE, Opcode.LT, Opcode.LE, Opcode.GT, Opcode.GE,
    Opcode.LOGIC_AND, Opcode.LOGIC_OR, Opcode.NEG, Opcode.LOGIC_NOT,
    Opcode.LOAD_ARR_1D, Opcode.LOAD_ARR_2D, Opcode.GET_FIELD, Opcode.CALL,
})


def op_name(operand: object) -> Optional[str]:
    """Symbolic name of a Var/Temp operand, else ``None``."""
    if isinstance(operand, (Var, Temp)):
        return str(operand)
    return None


def const_int_value(operand: object) -> Optional[int]:
    if (isinstance(operand, Constant) and operand.type_str in ("int", "char")
            and isinstance(operand.value, int) and not isinstance(operand.value, bool)):
        return int(operand.value)
    return None


def is_temp_name(name: Optional[str]) -> bool:
    return bool(name) and name[0] == "t" and name[1:].isdigit()


def defined_name(inst: TACInstruction) -> Optional[str]:
    """Name that ``inst`` fully (re)defines, or ``None`` (stores are excluded)."""
    if inst.opcode in _VALUE_PRODUCING:
        return op_name(inst.dst)
    return None


def wrap32(value: int) -> int:
    """Coerce a Python int to 32-bit two's-complement, matching a C ``int``."""
    value &= 0xFFFFFFFF
    if value >= 0x80000000:
        value -= 0x100000000
    return value


def c_div(a: int, b: int) -> int:
    """Integer division truncating toward zero (C99 ``/``)."""
    q = abs(a) // abs(b)
    return -q if (a < 0) != (b < 0) else q


def c_mod(a: int, b: int) -> int:
    """Remainder with the sign of the dividend (C99 ``%``)."""
    return a - c_div(a, b) * b


def program_global_names(program: Optional[TACProgram]) -> frozenset:
    """Names of module-level variables a function call is allowed to mutate."""
    if program is None:
        return frozenset()
    return frozenset(g[0] for g in program.global_vars)
