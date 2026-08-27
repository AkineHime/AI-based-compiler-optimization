"""Small shared helpers for the optimization passes.

Kept intentionally tiny -- just the bits that more than one pass needs and that
are easy to get subtly wrong (32-bit C integer semantics, the set of global
names a call may clobber).
"""
from typing import Optional

from ..ir.tac import TACProgram


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
