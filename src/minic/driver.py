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


def process_file(file_path: str, show_ast: bool = False, show_tac: bool = True, show_features: bool = False):
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
    parser.add_argument("--features", action="store_true", help="Print Extracted 18 Static Features (JSON)")

    args = parser.parse_args()
    process_file(args.file, show_ast=args.ast, show_tac=args.tac, show_features=args.features)


if __name__ == "__main__":
    main()
