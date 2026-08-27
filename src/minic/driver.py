import sys
import os
import json
import argparse
from .frontend.lexer import Lexer
from .frontend.parser import Parser
from .frontend.ast_printer import ASTPrinter
from .frontend.sema import SemanticAnalyzer
from .frontend.error_handler import MiniCError
from .ir.ir_generator import IRGenerator
from .ir.ir_printer import IRPrinter
from .features.extractor import FeatureExtractor


def process_file(file_path: str, show_ast: bool = False, show_tac: bool = True,
                 show_features: bool = False, optimize_combo: int = 0,
                 emit_c: bool = False, run: bool = False):
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

        # 5. Features
        extractor = FeatureExtractor()
        features = extractor.extract(ast, tac_prog)

        # 6. Optimization + Codegen (Person B)
        if optimize_combo or emit_c or run:
            from .optimizer import optimize as _optimize, combo_label
            from .codegen import emit_c as _emit_c
            opt_prog = _optimize(tac_prog, optimize_combo)
            c_source = _emit_c(opt_prog)
            if emit_c and not run:
                print(c_source)
            if run:
                from .pipeline import compile_and_run
                res = compile_and_run(c_source, optimize_combo)
                if not res.compiled:
                    print(res.compile_error, file=sys.stderr)
                    sys.exit(1)
                if res.stdout:
                    print(res.stdout, end="")
                print(f"[{combo_label(optimize_combo)}] exit code = "
                      f"{res.returncode}", file=sys.stderr)
            if not show_ast and not show_features and (emit_c or run):
                return

        if show_ast:
            print("=== Abstract Syntax Tree (AST) ===")
            print(ASTPrinter().print_ast(ast))
            print()

        if show_tac:
            print("=== Three-Address Code (TAC) ===")
            print(IRPrinter.format_program(tac_prog))

        if show_features:
            print("=== Extracted Static Features (18 metrics) ===")
            print(json.dumps(features, indent=2))

    except MiniCError as e:
        print(e, file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="MiniC Compiler Front-End and IR Pipeline")
    parser.add_argument("file", help="Path to .mc MiniC source file")
    parser.add_argument("--ast", action="store_true", help="Print Abstract Syntax Tree")
    parser.add_argument("--tac", action="store_true", default=True, help="Print Three-Address Code")
    parser.add_argument("--features", action="store_true", help="Print Extracted 19 Static Features (JSON)")
    parser.add_argument("--optimize", type=int, default=0, metavar="COMBO",
                        help="Apply optimization combo id 0..63 before codegen")
    parser.add_argument("--emit-c", action="store_true", dest="emit_c",
                        help="Emit generated C source")
    parser.add_argument("--run", action="store_true",
                        help="Compile emitted C with gcc -O0 and run it")

    args = parser.parse_args()
    show_tac = args.tac and not (args.emit_c or args.run)
    process_file(args.file, show_ast=args.ast, show_tac=show_tac,
                 show_features=args.features, optimize_combo=args.optimize,
                 emit_c=args.emit_c, run=args.run)


if __name__ == "__main__":
    main()
