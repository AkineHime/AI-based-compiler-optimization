import sys
import os
import json
import argparse
import shutil
import subprocess
import tempfile

# The AST tree and CFG printers use Unicode box-drawing glyphs; the default
# Windows console codepage (cp1252) can't encode them. Force UTF-8 output.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

from .frontend.lexer import Lexer
from .frontend.parser import Parser
from .frontend.ast_printer import ASTPrinter
from .frontend.sema import SemanticAnalyzer
from .frontend.error_handler import MiniCError
from .ir.ir_generator import IRGenerator
from .ir.ir_printer import IRPrinter
from .ir.cfg import build_cfg_for_function
from .features import all_features
from .optimizer.pass_manager import optimize_program, get_pass_names
from .codegen.c_emitter import CEmitter


def process_file(
    file_path: str,
    show_ast: bool = False,
    show_tree: bool = False,
    show_tac: bool = False,
    show_cfg: bool = False,
    show_features: bool = False,
    optimize_combo: int = 0,
    emit_c: bool = False,
    run_binary: bool = False,
):
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        # 1. Lex
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        # 2. Parse
        parser = Parser(tokens, source)
        ast = parser.parse()

        # 3. Semantic Analysis
        sema = SemanticAnalyzer(source)
        sema.analyze(ast)

        # 4. IR Generation
        ir_gen = IRGenerator()
        tac_prog = ir_gen.generate(ast)

        # 5. Features (19 structural + 8 opportunity = the 27 the ML model reads)
        features = all_features(ast, tac_prog)

        if show_ast:
            print("=== Abstract Syntax Tree (AST Indented) ===")
            print(ASTPrinter().print_ast(ast))
            print()

        if show_tree:
            print("=== Abstract Syntax Tree (Visual Branch Tree) ===")
            print(ASTPrinter().print_tree(ast))
            print()

        # 6. Apply Optimization Passes (if any requested)
        if optimize_combo > 0:
            pass_names = get_pass_names(optimize_combo)
            print(f"=== Applying Optimization Combo {optimize_combo} ({', '.join(pass_names)}) ===")
            tac_prog = optimize_program(tac_prog, optimize_combo)

        if show_tac:
            print("=== Three-Address Code (TAC) ===")
            print(IRPrinter.format_program(tac_prog))
            print()

        if show_cfg:
            print("=== Control Flow Graphs (CFG per Function) ===")
            for func in tac_prog.functions:
                cfg = build_cfg_for_function(func)
                print(f"--- Function: {func.name} (Blocks: {len(cfg.blocks)}, Loops: {len(cfg.loops)}, Max Depth: {cfg.get_max_loop_depth()}) ---")
                print(cfg.to_ascii_tree())
                print("\nMermaid Flowchart:")
                print("```mermaid")
                print(cfg.to_mermaid(func.name))
                print("```\n")

        if show_features:
            print("=== Extracted Features (19 structural + 8 opportunity) ===")
            print(json.dumps(features, indent=2))
            print()

        # 7. Codegen (IR-to-C)
        emitter = CEmitter()
        c_code = emitter.emit(tac_prog)

        if emit_c:
            print("=== Emitted C Code ===")
            print(c_code)
            print()

        # 8. Compile and Run with GCC
        if run_binary:
            workdir = tempfile.mkdtemp(prefix="minic_driver_")
            c_file = os.path.join(workdir, "out.c")
            bin_file = os.path.join(workdir, "out" + (".exe" if os.name == "nt" else ""))
            with open(c_file, "w", encoding="utf-8") as f:
                f.write(c_code)

            try:
                comp = subprocess.run(["gcc", "-O0", "-o", bin_file, c_file], capture_output=True, text=True)
                if comp.returncode != 0:
                    print("Compilation Error:\n", comp.stderr, file=sys.stderr)
                    sys.exit(1)

                run = subprocess.run([bin_file])
                print(f"Program exited with return code: {run.returncode}")
            finally:
                shutil.rmtree(workdir, ignore_errors=True)

    except MiniCError as e:
        print(e, file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="MiniC Compiler Front-End, IR, Optimizer, and Codegen Pipeline")
    parser.add_argument("file", help="Path to .mc MiniC source file")
    parser.add_argument("--tree", action="store_true", help="Print visual AST tree diagram with branch glyphs")
    parser.add_argument("--ast", action="store_true", help="Print Abstract Syntax Tree (indented text)")
    parser.add_argument("--tac", action="store_true", help="Print Three-Address Code")
    parser.add_argument("--cfg", action="store_true", help="Print visual Control Flow Graph (CFG) and Mermaid diagrams")
    parser.add_argument("--features", action="store_true", help="Print the 27 extracted features (19 structural + 8 opportunity), JSON")
    parser.add_argument("--optimize", type=int, default=0, help="6-bit combo mask (0..63): CF DCE CSE LICM SR LU")
    parser.add_argument("--emit-c", action="store_true", help="Emit value-semantics C code")
    parser.add_argument("--run", action="store_true", help="Compile emitted C with gcc -O0 and run")

    args = parser.parse_args()

    show_tac = args.tac or (not args.ast and not args.tree and not args.cfg and not args.features and not args.emit_c and not args.run)

    process_file(
        args.file,
        show_ast=args.ast,
        show_tree=args.tree,
        show_tac=show_tac,
        show_cfg=args.cfg,
        show_features=args.features,
        optimize_combo=args.optimize,
        emit_c=args.emit_c,
        run_binary=args.run,
    )


if __name__ == "__main__":
    main()
