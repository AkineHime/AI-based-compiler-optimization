"""MiniC Intermediate Representation (TAC, CFG, and Lowering)."""

from .tac import Opcode, Operand, Temp, Var, Constant, Label, TACInstruction, TACFunction, TACProgram
from .cfg import BasicBlock, CFG, build_cfg_for_function
from .ir_generator import IRGenerator
from .ir_printer import IRPrinter

__all__ = [
    "Opcode",
    "Operand",
    "Temp",
    "Var",
    "Constant",
    "Label",
    "TACInstruction",
    "TACFunction",
    "TACProgram",
    "BasicBlock",
    "CFG",
    "build_cfg_for_function",
    "IRGenerator",
    "IRPrinter",
]
