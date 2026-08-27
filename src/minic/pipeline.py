"""Convenience end-to-end helpers: MiniC source -> optimized C -> run.

Keeps the front-end wiring in one place so the optimizer, codegen and the
correctness harness all go through an identical path.
"""
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from typing import Optional

from .frontend.lexer import Lexer
from .frontend.parser import Parser
from .frontend.sema import SemanticAnalyzer
from .ir.ir_generator import IRGenerator
from .ir.tac import TACProgram
from .optimizer import optimize_program
from .codegen import CEmitter


def source_to_tac(source: str) -> TACProgram:
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens, source).parse()
    SemanticAnalyzer(source).analyze(ast)
    return IRGenerator().generate(ast)


def source_to_c(source: str, combo_id: int = 0) -> str:
    tac = source_to_tac(source)
    tac = optimize_program(tac, combo_id)
    return CEmitter().emit(tac)


@dataclass
class RunResult:
    combo_id: int
    compiled: bool
    returncode: Optional[int]
    stdout: str
    stderr: str
    compile_error: str = ""


def compile_and_run(c_source: str, combo_id: int = 0,
                    gcc: str = "gcc", timeout: float = 30.0,
                    workdir: Optional[str] = None) -> RunResult:
    tmp = workdir or tempfile.mkdtemp(prefix="minic_")
    c_path = os.path.join(tmp, f"combo_{combo_id:02d}.c")
    exe_path = os.path.join(tmp, f"combo_{combo_id:02d}"
                            + (".exe" if os.name == "nt" else ""))
    with open(c_path, "w", encoding="utf-8") as fh:
        fh.write(c_source)

    cp = subprocess.run(
        [gcc, "-O0", "-std=c99", "-w", c_path, "-o", exe_path],
        capture_output=True, text=True, timeout=timeout,
    )
    if cp.returncode != 0:
        return RunResult(combo_id, False, None, "", "", cp.stderr)

    rp = subprocess.run([exe_path], capture_output=True, text=True,
                        timeout=timeout)
    return RunResult(combo_id, True, rp.returncode, rp.stdout, rp.stderr)


def main(argv=None) -> int:
    import argparse
    p = argparse.ArgumentParser(description="MiniC optimize + codegen pipeline")
    p.add_argument("file")
    p.add_argument("--combo", type=int, default=0, help="combo id 0..63")
    p.add_argument("--run", action="store_true", help="compile with gcc -O0 and run")
    args = p.parse_args(argv)

    with open(args.file, "r", encoding="utf-8") as fh:
        source = fh.read()
    c_source = source_to_c(source, args.combo)
    if not args.run:
        sys.stdout.write(c_source)
        return 0

    res = compile_and_run(c_source, args.combo)
    if not res.compiled:
        sys.stderr.write(res.compile_error + "\n")
        return 1
    sys.stdout.write(res.stdout)
    print(f"[combo {args.combo}] exit code = {res.returncode}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
