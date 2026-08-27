"""minic-opt -- recommend and demonstrate optimization combos for a MiniC file.

    python -m demo.cli recommend  benchmarks/loops/licm_arith.mc
    python -m demo.cli benchmark  benchmarks/loops/licm_arith.mc [--combo N]
"""
import argparse
import os
import sys

from src.minic.frontend.lexer import Lexer
from src.minic.frontend.parser import Parser
from src.minic.frontend.sema import SemanticAnalyzer
from src.minic.ir.ir_generator import IRGenerator
from src.minic.features import all_features
from src.minic.optimizer import optimize_program
from src.minic.optimizer.pass_manager import get_pass_names
from src.minic.codegen import CEmitter
from src.minic.harness.compiler import compile_c, cleanup
from src.minic.harness.timer import measure_execution_time

DEFAULT_MODEL = "data/trained_model.pkl"


def _frontend(path):
    src = open(path, encoding="utf-8").read()
    ast = Parser(Lexer(src).tokenize(), src).parse()
    SemanticAnalyzer(src).analyze(ast)
    tac = IRGenerator().generate(ast)
    return ast, tac


def _time_combo(tac, combo, runs, warmup, expected=None):
    c_src = CEmitter().emit(optimize_program(tac, combo))
    cr = compile_c(c_src, tag=f"cli_{combo}")
    if not cr.ok:
        raise SystemExit(f"gcc failed for combo {combo}:\n{cr.stderr}")
    tr = measure_execution_time(cr.binary_path, expected_exit_code=expected,
                                runs=runs, warmup=warmup)
    cleanup(cr.c_path, cr.binary_path)
    return tr


def cmd_recommend(args):
    ast, tac = _frontend(args.file)
    feats = all_features(ast, tac)

    print(f"# {os.path.basename(args.file)}")
    print("\nstatic features (19):")
    for k, v in feats.items():
        print(f"  {k:30s} {v:g}")

    if os.path.exists(args.model):
        from src.minic.ml import SpeedupModel, recommend_combo, rank_combos
        model = SpeedupModel.load(args.model)
        combo, pred, names = recommend_combo(feats, model)
        print(f"\nML-recommended combo: {combo}  "
              f"[{', '.join(names) or 'baseline'}]   predicted speedup x{pred:.3f}")
        print("top 5 predicted:")
        for c, p in rank_combos(feats, model):
            print(f"  combo {c:2d}  x{p:.3f}  [{', '.join(get_pass_names(c)) or 'baseline'}]")
    else:
        print(f"\n(no trained model at {args.model}; run  python -m src.minic.ml.train)")

    if args.verify:
        _verify(tac, combo if os.path.exists(args.model) else 63, args)


def _verify(tac, combo, args):
    base = _time_combo(tac, 0, args.runs, args.warmup)
    opt = _time_combo(tac, combo, args.runs, args.warmup, expected=base.exit_code)
    print(f"\nmeasured:  baseline {base.median_ms:.2f} ms   "
          f"combo {combo} {opt.median_ms:.2f} ms   "
          f"speedup x{base.median_ms / opt.median_ms:.3f}   "
          f"(exit {base.exit_code}, match {opt.exit_code == base.exit_code})")


def cmd_benchmark(args):
    ast, tac = _frontend(args.file)
    base = _time_combo(tac, 0, args.runs, args.warmup)
    combos = [args.combo] if args.combo is not None else [1, 2, 4, 8, 16, 32, 63]
    print(f"# {os.path.basename(args.file)}   baseline (combo 0) = {base.median_ms:.2f} ms  "
          f"exit {base.exit_code}")
    best = (0, base.median_ms)
    for c in combos:
        tr = _time_combo(tac, c, args.runs, args.warmup, expected=base.exit_code)
        tag = "".join(k for k, b in zip("CDSLRU", [c & 1, c & 2, c & 4, c & 8, c & 16, c & 32]) if b) or "-"
        print(f"  combo {c:2d} [{tag:5s}]  {tr.median_ms:8.2f} ms   x{base.median_ms / tr.median_ms:.3f}")
        if tr.median_ms < best[1]:
            best = (c, tr.median_ms)
    print(f"\nbest: combo {best[0]}  x{base.median_ms / best[1]:.3f}  "
          f"[{', '.join(get_pass_names(best[0])) or 'baseline'}]")


def main(argv=None):
    p = argparse.ArgumentParser(prog="minic-opt")
    p.add_argument("--runs", type=int, default=12)
    p.add_argument("--warmup", type=int, default=3)
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("recommend", help="show features + ML-recommended combo")
    r.add_argument("file")
    r.add_argument("--model", default=DEFAULT_MODEL)
    r.add_argument("--verify", action="store_true", help="also compile & time it")
    r.set_defaults(func=cmd_recommend)

    b = sub.add_parser("benchmark", help="time a file across optimization combos")
    b.add_argument("file")
    b.add_argument("--combo", type=int, default=None)
    b.set_defaults(func=cmd_benchmark)

    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
