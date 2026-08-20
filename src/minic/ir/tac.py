from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Union


class Opcode(Enum):
    # Data Movement
    ASSIGN = auto()          # dst = src1

    # Arithmetic
    ADD = auto()             # dst = src1 + src2
    SUB = auto()             # dst = src1 - src2
    MUL = auto()             # dst = src1 * src2
    DIV = auto()             # dst = src1 / src2
    MOD = auto()             # dst = src1 % src2
    NEG = auto()             # dst = -src1

    # Relational
    EQ = auto()              # dst = src1 == src2
    NE = auto()              # dst = src1 != src2
    LT = auto()              # dst = src1 < src2
    LE = auto()              # dst = src1 <= src2
    GT = auto()              # dst = src1 > src2
    GE = auto()              # dst = src1 >= src2

    # Logical
    LOGIC_AND = auto()       # dst = src1 && src2
    LOGIC_OR = auto()        # dst = src1 || src2
    LOGIC_NOT = auto()       # dst = !src1

    # Control Flow
    LABEL = auto()           # LABEL L:
    JUMP = auto()            # goto L
    JUMP_IF_TRUE = auto()    # if src1 goto L
    JUMP_IF_FALSE = auto()   # ifFalse src1 goto L

    # Functions
    PARAM = auto()           # param src1
    CALL = auto()            # dst = call func_name, n_args (dst can be None for void calls)
    RETURN = auto()          # return src1 (src1 can be None)

    # Memory / Aggregate Access (Value Semantics)
    LOAD_ARR_1D = auto()     # dst = arr[idx]
    STORE_ARR_1D = auto()    # arr[idx] = src1
    LOAD_ARR_2D = auto()     # dst = arr[i][j]
    STORE_ARR_2D = auto()    # arr[i][j] = src1
    GET_FIELD = auto()       # dst = struct_var.field
    SET_FIELD = auto()       # struct_var.field = src1

    # Declarations / Allocations
    ALLOC_LOCAL = auto()     # alloc name, type_info
    COMMENT = auto()         # // text


class Operand:
    """Base class for TAC operands."""
    pass


@dataclass(frozen=True)
class Temp(Operand):
    id: int
    type_str: str = "int"

    def __str__(self) -> str:
        return f"t{self.id}"


@dataclass(frozen=True)
class Var(Operand):
    name: str
    type_str: str = "int"

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Constant(Operand):
    value: Any
    type_str: str = "int"

    def __str__(self) -> str:
        if self.type_str == "string":
            return f'"{self.value}"'
        elif self.type_str == "char":
            return f"'{self.value}'"
        return str(self.value)


@dataclass(frozen=True)
class Label(Operand):
    name: str

    def __str__(self) -> str:
        return self.name


@dataclass
class TACInstruction:
    opcode: Opcode
    dst: Optional[Operand] = None
    src1: Optional[Union[Operand, Any]] = None
    src2: Optional[Union[Operand, Any]] = None
    src3: Optional[Union[Operand, Any]] = None  # Used for 2D array stores/loads if needed
    annotation: str = ""

    def __str__(self) -> str:
        op = self.opcode

        if op == Opcode.LABEL:
            return f"{self.dst}:"
        elif op == Opcode.JUMP:
            return f"    goto {self.dst}"
        elif op == Opcode.JUMP_IF_TRUE:
            return f"    if {self.src1} goto {self.dst}"
        elif op == Opcode.JUMP_IF_FALSE:
            return f"    ifFalse {self.src1} goto {self.dst}"
        elif op == Opcode.ASSIGN:
            return f"    {self.dst} = {self.src1}"
        elif op in (Opcode.ADD, Opcode.SUB, Opcode.MUL, Opcode.DIV, Opcode.MOD,
                    Opcode.EQ, Opcode.NE, Opcode.LT, Opcode.LE, Opcode.GT, Opcode.GE,
                    Opcode.LOGIC_AND, Opcode.LOGIC_OR):
            op_symbols = {
                Opcode.ADD: "+", Opcode.SUB: "-", Opcode.MUL: "*", Opcode.DIV: "/", Opcode.MOD: "%",
                Opcode.EQ: "==", Opcode.NE: "!=", Opcode.LT: "<", Opcode.LE: "<=", Opcode.GT: ">", Opcode.GE: ">=",
                Opcode.LOGIC_AND: "&&", Opcode.LOGIC_OR: "||"
            }
            return f"    {self.dst} = {self.src1} {op_symbols[op]} {self.src2}"
        elif op == Opcode.NEG:
            return f"    {self.dst} = -{self.src1}"
        elif op == Opcode.LOGIC_NOT:
            return f"    {self.dst} = !{self.src1}"
        elif op == Opcode.PARAM:
            return f"    param {self.src1}"
        elif op == Opcode.CALL:
            if self.dst:
                return f"    {self.dst} = call {self.src1}, {self.src2}"
            return f"    call {self.src1}, {self.src2}"
        elif op == Opcode.RETURN:
            if self.src1:
                return f"    return {self.src1}"
            return "    return"
        elif op == Opcode.LOAD_ARR_1D:
            return f"    {self.dst} = {self.src1}[{self.src2}]"
        elif op == Opcode.STORE_ARR_1D:
            return f"    {self.dst}[{self.src1}] = {self.src2}"
        elif op == Opcode.LOAD_ARR_2D:
            return f"    {self.dst} = {self.src1}[{self.src2}][{self.src3}]"
        elif op == Opcode.STORE_ARR_2D:
            return f"    {self.dst}[{self.src1}][{self.src2}] = {self.src3}"
        elif op == Opcode.GET_FIELD:
            return f"    {self.dst} = {self.src1}.{self.src2}"
        elif op == Opcode.SET_FIELD:
            return f"    {self.dst}.{self.src1} = {self.src2}"
        elif op == Opcode.ALLOC_LOCAL:
            return f"    alloc {self.dst} : {self.src1}"
        elif op == Opcode.COMMENT:
            return f"    // {self.annotation}"

        return f"    {self.opcode.name} {self.dst}, {self.src1}, {self.src2}"


@dataclass
class TACFunction:
    name: str
    return_type: str
    params: List[Tuple[str, str]] = field(default_factory=list)  # (param_name, type_str)
    instructions: List[TACInstruction] = field(default_factory=list)
    local_types: Dict[str, str] = field(default_factory=dict)     # name -> type_str


@dataclass
class TACProgram:
    structs: Dict[str, Dict[str, str]] = field(default_factory=dict)  # struct_name -> {field_name: type_str}
    global_vars: List[Tuple[str, str, Optional[Any]]] = field(default_factory=list)  # (name, type_str, init_val)
    functions: List[TACFunction] = field(default_factory=list)
