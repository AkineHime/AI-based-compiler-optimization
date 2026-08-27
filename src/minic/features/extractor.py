from typing import Dict, List, Set, Any
from ..frontend.ast_nodes import Program, Literal
from ..ir.tac import TACProgram, TACFunction, Opcode, Constant, Var, Temp
from ..ir.cfg import build_cfg_for_function, CFG


FEATURE_NAMES: List[str] = [
    "total_instructions",
    "basic_block_count",
    "loop_count",
    "max_loop_depth",
    "branch_count",
    "branch_density",
    "arithmetic_ops_count",
    "multiplication_count",
    "constant_load_count",
    "array_access_count",
    "array_2d_access_count",
    "struct_access_count",
    "function_call_count",
    "recursive_call_count",
    "named_variable_count",
    "temp_variable_count",
    "string_ops_count",
    "instruction_density_in_loops",
    "cyclomatic_complexity",
]


class FeatureExtractor:
    """Extracts 19 static features from AST and TAC/CFG representations.

    Note: the original ``variable_count`` feature has been split into
    ``named_variable_count`` (source-level locals, params and globals) and
    ``temp_variable_count`` (compiler-generated ``tN`` temporaries), since the
    two behave very differently under optimization and the split is far easier
    to introduce before any dataset rows exist than after.
    """

    def __init__(self):
        pass

    def extract(self, ast_prog: Program, tac_prog: TACProgram) -> Dict[str, float]:
        """Extract static feature dictionary from AST and TAC."""
        features: Dict[str, float] = {name: 0.0 for name in FEATURE_NAMES}

        total_instructions = 0
        total_bb_count = 0
        total_loop_count = 0
        max_loop_depth = 0
        branch_count = 0
        arithmetic_ops_count = 0
        multiplication_count = 0
        constant_load_count = 0
        array_access_count = 0
        array_2d_access_count = 0
        struct_access_count = 0
        function_call_count = 0
        recursive_call_count = 0
        unique_named_vars: Set[str] = set()
        unique_temps: Set[str] = set()
        string_ops_count = 0
        loop_instructions_count = 0
        total_cyclomatic = 0

        # Scan global vars
        for g_name, g_type, init_val in tac_prog.global_vars:
            unique_named_vars.add(g_name)
            if isinstance(init_val, str):
                string_ops_count += 1

        # Function parameters are source-level named variables too
        for func in tac_prog.functions:
            for p_name, _p_type in func.params:
                unique_named_vars.add(p_name)

        # Process each TAC function
        for func in tac_prog.functions:
            cfg = build_cfg_for_function(func)

            # Basic block count
            total_bb_count += len(cfg.blocks)

            # Loops
            total_loop_count += len(cfg.loops)
            func_max_depth = cfg.get_max_loop_depth()
            if func_max_depth > max_loop_depth:
                max_loop_depth = func_max_depth

            # Collect blocks in loops
            loop_block_ids: Set[int] = set()
            for loop in cfg.loops:
                for b in loop.blocks:
                    loop_block_ids.add(b.id)

            # Calculate cyclomatic complexity: E - N + 2P (P=1 for single function)
            num_nodes = len(cfg.blocks)
            num_edges = sum(len(b.successors) for b in cfg.blocks)
            if num_nodes > 0:
                total_cyclomatic += max(1, num_edges - num_nodes + 2)

            # Inspect instructions
            for inst in func.instructions:
                total_instructions += 1

                # Variables & Temporaries
                for operand in (inst.dst, inst.src1, inst.src2, inst.src3):
                    if isinstance(operand, Temp):
                        unique_temps.add(str(operand))
                    elif isinstance(operand, Var):
                        unique_named_vars.add(str(operand))

                # Branches
                if inst.opcode in (Opcode.JUMP_IF_TRUE, Opcode.JUMP_IF_FALSE):
                    branch_count += 1

                # Arithmetic
                if inst.opcode in (Opcode.ADD, Opcode.SUB, Opcode.MUL, Opcode.DIV, Opcode.MOD):
                    arithmetic_ops_count += 1
                    if inst.opcode == Opcode.MUL:
                        multiplication_count += 1

                # Constants
                if isinstance(inst.src1, Constant) or isinstance(inst.src2, Constant):
                    constant_load_count += 1
                    if isinstance(inst.src1, Constant) and inst.src1.type_str == "string":
                        string_ops_count += 1

                # Arrays
                if inst.opcode in (Opcode.LOAD_ARR_1D, Opcode.STORE_ARR_1D):
                    array_access_count += 1
                elif inst.opcode in (Opcode.LOAD_ARR_2D, Opcode.STORE_ARR_2D):
                    array_access_count += 1
                    array_2d_access_count += 1

                # Structs
                if inst.opcode in (Opcode.GET_FIELD, Opcode.SET_FIELD):
                    struct_access_count += 1

                # Calls
                if inst.opcode == Opcode.CALL:
                    function_call_count += 1
                    called_func_name = str(inst.src1)
                    if called_func_name == func.name:
                        recursive_call_count += 1

            # Count instructions inside loops
            for b in cfg.blocks:
                if b.id in loop_block_ids:
                    loop_instructions_count += len(b.instructions)

        # Derive ratios
        branch_density = (branch_count / total_instructions) if total_instructions > 0 else 0.0
        loop_density = (loop_instructions_count / total_instructions) if total_instructions > 0 else 0.0

        features["total_instructions"] = float(total_instructions)
        features["basic_block_count"] = float(total_bb_count)
        features["loop_count"] = float(total_loop_count)
        features["max_loop_depth"] = float(max_loop_depth)
        features["branch_count"] = float(branch_count)
        features["branch_density"] = float(round(branch_density, 4))
        features["arithmetic_ops_count"] = float(arithmetic_ops_count)
        features["multiplication_count"] = float(multiplication_count)
        features["constant_load_count"] = float(constant_load_count)
        features["array_access_count"] = float(array_access_count)
        features["array_2d_access_count"] = float(array_2d_access_count)
        features["struct_access_count"] = float(struct_access_count)
        features["function_call_count"] = float(function_call_count)
        features["recursive_call_count"] = float(recursive_call_count)
        features["named_variable_count"] = float(len(unique_named_vars))
        features["temp_variable_count"] = float(len(unique_temps))
        features["string_ops_count"] = float(string_ops_count)
        features["instruction_density_in_loops"] = float(round(loop_density, 4))
        features["cyclomatic_complexity"] = float(total_cyclomatic)

        return features

    def extract_vector(self, ast_prog: Program, tac_prog: TACProgram) -> List[float]:
        """Return feature values in standardized list format."""
        feature_dict = self.extract(ast_prog, tac_prog)
        return [feature_dict[name] for name in FEATURE_NAMES]
