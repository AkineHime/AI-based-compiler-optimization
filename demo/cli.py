"""minic-opt -- recommend and demonstrate optimization combos for a MiniC file.

    python -m demo.cli recommend benchmarks/loops/licm_arith.mc [--verify] [--features]
    python -m demo.cli benchmark benchmarks/loops/licm_arith.mc [--combo N] [--runs 12]

(`python minic.py recommend ...` / `python minic.py benchmark ...` are the same commands.)
"""
import argparse
import os
import sys

from src.minic.frontend.lexer import Lexer
from src.minic.frontend.parser import Parser
from src.minic.frontend.sema import SemanticAnalyzer
from src.minic.frontend.error_handler import MiniCError
from src.minic.ir.ir_generator import IRGenerator
from src.minic.features import all_features
from src.minic.optimizer import optimize_program
from src.minic.optimizer.pass_manager import get_pass_names, get_pass_abbrs
from src.minic.codegen import CEmitter
from src.minic.harness.compiler import compile_c, cleanup
from src.minic.harness.timer import measure_execution_time
from src.minic.ml.predictor import DEFAULT_MODEL_PATH


def _passes(combo: int) -> str:
    return ", ".join(get_pass_abbrs(combo)) or "no passes"


def _frontend(path):
    if not os.path.exists(path):
        raise SystemExit(f"error: file not found: {path}")
    src = open(path, encoding="utf-8").read()
    try:
        ast = Parser(Lexer(src).tokenize(), src).parse()
        SemanticAnalyzer(src).analyze(ast)
    except MiniCError as e:
        raise SystemExit(str(e))
    return ast, IRGenerator().generate(ast)


def _time_combo(tac, combo, runs, warmup, expected=None):
    c_src = CEmitter().emit(optimize_program(tac, combo))
    cr = compile_c(c_src, tag=f"cli_{combo}")
    if not cr.ok:
        raise SystemExit(f"error: gcc failed for combo {combo}:\n{cr.stderr}")
    try:
        return measure_execution_time(cr.binary_path, expected_exit_code=expected,
                                      runs=runs, warmup=warmup)
    finally:
        cleanup(cr.c_path, cr.binary_path)


def cmd_recommend(args):
    ast, tac = _frontend(args.file)
    feats = all_features(ast, tac)
    print(f"# {os.path.basename(args.file)}")
    if args.features:
        print(f"\nstatic + opportunity features ({len(feats)}):")
        for k, v in feats.items():
            print(f"  {k:30s} {v:g}")

    from src.minic.ml import load_or_train, recommend_combo, rank_combos
    model = load_or_train(args.model)
    combo, pred, names = recommend_combo(feats, model)
    note = ""
    if model.metadata.get("strategy") == "margin" and combo == 0:
        note = (f"\n  (the model abstained: no combo was predicted to beat "
                f"x{1 + model.metadata['margin']:.2f}, so it leaves the program alone)")
    print(f"\nrecommended: combo {combo} [{_passes(combo)}]   "
          f"predicted speedup x{pred:.3f}{note}")
    print("\ntop 5 predicted combos:")
    for c, p in rank_combos(feats, model):
        print(f"  combo {c:2d}  x{p:.3f}  [{_passes(c)}]")
    if args.verify:
        _verify(tac, combo, args)
    else:
        print("\n(add --verify to compile both versions and time them)")


def _verify(tac, combo, args):
    print(f"\ntiming no passes vs combo {combo} ({args.runs} runs each)...")
    base = _time_combo(tac, 0, args.runs, args.warmup)
    opt = _time_combo(tac, combo, args.runs, args.warmup, expected=base.exit_code)
    same = opt.exit_code == base.exit_code
    print(f"measured:  no passes {base.median_ms:.2f} ms   combo {combo} {opt.median_ms:.2f} ms"
          f"   speedup x{base.median_ms / opt.median_ms:.3f}")
    print(f"result check: both builds returned {base.exit_code}" if same else
          f"RESULT MISMATCH: {base.exit_code} vs {opt.exit_code}")


def cmd_benchmark(args):
    ast, tac = _frontend(args.file)
    base = _time_combo(tac, 0, args.runs, args.warmup)
    combos = [args.combo] if args.combo is not None else [1, 2, 4, 8, 16, 32, 63]
    print(f"# {os.path.basename(args.file)}   no passes (combo 0) = {base.median_ms:.2f} ms  "
          f"returns {base.exit_code}\n")
    best = (0, base.median_ms)
    for c in combos:
        tr = _time_combo(tac, c, args.runs, args.warmup, expected=base.exit_code)
        print(f"  combo {c:2d}  {tr.median_ms:8.2f} ms   x{base.median_ms / tr.median_ms:.3f}"
              f"   [{_passes(c)}]")
        if tr.median_ms < best[1]:
            best = (c, tr.median_ms)
    print(f"\nfastest: combo {best[0]}  x{base.median_ms / best[1]:.3f}  "
          f"[{', '.join(get_pass_names(best[0])) or 'no passes'}]")


def build_parser():
    timing = argparse.ArgumentParser(add_help=False)
    timing.add_argument("--runs", type=int, default=12, help="timed runs per build (default 12)")
    timing.add_argument("--warmup", type=int, default=3, help="untimed warm-up runs (default 3)")

    p = argparse.ArgumentParser(prog="minic-opt", description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("recommend", parents=[timing],
                       help="ask the ML model which passes to enable for a file")
    r.add_argument("file", help="MiniC source file (.mc)")
    r.add_argument("--verify", action="store_true",
                   help="also compile with and without the passes and time both")
    r.add_argument("--features", action="store_true", help="print the 27 input features")
    r.add_argument("--model", default=DEFAULT_MODEL_PATH, help=argparse.SUPPRESS)
    r.set_defaults(func=cmd_recommend)

    b = sub.add_parser("benchmark", parents=[timing],
                       help="time a file with each pass alone and with all passes")
    b.add_argument("file", help="MiniC source file (.mc)")
    b.add_argument("--combo", type=int, default=None, help="time only this combo (0-63)")
    b.set_defaults(func=cmd_benchmark)
    return p


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    args = build_parser().parse_args(argv)
    if getattr(args, "combo", None) is not None and not 0 <= args.combo <= 63:
        raise SystemExit("error: --combo must be between 0 and 63")
    args.func(args)


if __name__ == "__main__":
    main()
