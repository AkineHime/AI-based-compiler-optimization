from typing import List
from .tac import TACProgram, TACFunction


class IRPrinter:
    """Formats TACProgram and TACFunction into readable Three-Address Code."""

    @staticmethod
    def format_program(program: TACProgram) -> str:
        lines: List[str] = []

        # Struct definitions
        if program.structs:
            lines.append("// --- Struct Definitions ---")
            for struct_name, fields in program.structs.items():
                lines.append(f"struct {struct_name} {{")
                for f_name, f_type in fields.items():
                    lines.append(f"    {f_type} {f_name};")
                lines.append("};")
            lines.append("")

        # Global variables
        if program.global_vars:
            lines.append("// --- Global Variables ---")
            for g_name, g_type, init_val in program.global_vars:
                if init_val is not None:
                    lines.append(f"global {g_name} : {g_type} = {init_val}")
                else:
                    lines.append(f"global {g_name} : {g_type}")
            lines.append("")

        # Functions
        for func in program.functions:
            lines.append(IRPrinter.format_function(func))
            lines.append("")

        return "\n".join(lines)

    @staticmethod
    def format_function(func: TACFunction) -> str:
        lines: List[str] = []
        params_str = ", ".join(f"{p_name}: {p_type}" for p_name, p_type in func.params)
        lines.append(f"func {func.name}({params_str}) -> {func.return_type}:")

        for inst in func.instructions:
            lines.append(str(inst))

        return "\n".join(lines)
