"""MiniC Playground -- a browser code editor that compiles MiniC two ways
(unoptimized, and with the ML-recommended pass combo) and shows the speedup.

    python -m demo.app          # serves http://127.0.0.1:5005

No framework magic: one Flask route serves the page, one JSON endpoint runs the
pipeline.  MiniC has no I/O, so a program's observable result is its return
value (process exit code); both builds must agree on it.
"""
import io
import os
import sys
import time
import traceback

from flask import Flask, jsonify, request, send_from_directory

from src.minic.frontend.lexer import Lexer
from src.minic.frontend.parser import Parser
from src.minic.frontend.sema import SemanticAnalyzer
from src.minic.frontend.error_handler import MiniCError
from src.minic.ir.ir_generator import IRGenerator
from src.minic.ir.ir_printer import IRPrinter
from src.minic.features import all_features
from src.minic.optimizer import optimize_program
from src.minic.optimizer.pass_manager import (
    PassManager, get_pass_names, get_pass_abbrs, PASS_FLAGS, NUM_COMBOS,
)
from src.minic.codegen import CEmitter
from src.minic.harness.compiler import compile_c, cleanup
from src.minic.harness.timer import measure_execution_time

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(os.path.dirname(HERE), "data", "trained_model.pkl")

app = Flask(__name__, static_folder=os.path.join(HERE, "static"))

_MODEL = None
_MODEL_ERR = None
try:
    from src.minic.ml.model import SpeedupModel
    from src.minic.ml.predictor import recommend_combo
    if os.path.exists(MODEL_PATH):
        _MODEL = SpeedupModel.load(MODEL_PATH)
except Exception as e:  # noqa: BLE001
    _MODEL_ERR = str(e)


EXAMPLES = {
    "loop-invariant math": """int main() {
    int a = 123;
    int b = 45;
    int c = 67;
    int acc = 0;
    int i = 0;
    while (i < 40000000) {
        acc = acc + a * b + c * a + a * a + b * b + a * b * c;
        i = i + 1;
    }
    return ((acc % 251) + 251) % 251;
}
""",
    "redundant divides (CSE)": """int main() {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < 12000000) {
        int u = (x * 7919) % 10007;
        int v = (x * 7919) % 10007;
        int w = (x * 7919) % 10007;
        acc = acc + u + v + w;
        x = x + 3;
        i = i + 1;
    }
    return ((acc % 251) + 251) % 251;
}
""",
    "struct distance (LICM + CF)": """struct Pt { int x; int y; };
int main() {
    struct Pt a;
    struct Pt b;
    a.x = 33; a.y = 71;
    b.x = 9;  b.y = 24;
    int acc = 0;
    int i = 0;
    while (i < 35000000) {
        int dx = a.x - b.x;
        int dy = a.y - b.y;
        acc = acc + dx * dx + dy * dy + dx * dy;
        i = i + 1;
    }
    return ((acc % 251) + 251) % 251;
}
""",
    "recursion (little to optimize)": """int fib(int n) {
    if (n < 2) { return n; }
    return fib(n - 1) + fib(n - 2);
}
int main() {
    int s = 0;
    int r = 0;
    while (r < 5) { s = s + fib(30); r = r + 1; }
    return ((s % 251) + 251) % 251;
}
""",
    "canonical example (returns 83)": open(
        os.path.join(os.path.dirname(HERE), "canonical_example.mc"), encoding="utf-8"
    ).read(),
}


def _frontend(source: str):
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens, source).parse()
    SemanticAnalyzer(source).analyze(ast)
    tac = IRGenerator().generate(ast)
    return ast, tac


def _pass_activity(tac, combo: int):
    """Run each enabled pass alone and report how much of the IR it rewrote."""
    from src.minic.optimizer import (
        constant_folding, dce, cse, licm, strength_reduction, loop_unroll,
    )
    import copy
    steps = [
        (1, "Constant Folding", lambda f: constant_folding.constant_folding_pass(f)),
        (4, "Common Subexpr. Elim.", lambda f: cse.cse_pass(f)),
        (32, "Loop Unrolling", lambda f: loop_unroll.loop_unroll_pass(f)),
        (8, "Loop-Invariant Code Motion", lambda f: licm.licm_pass(f)),
        (16, "Strength Reduction", lambda f: strength_reduction.strength_reduction_pass(f)),
        (2, "Dead Code Elimination", lambda f: dce.dce_pass(f)),
    ]
    rows = []
    for func in tac.functions:
        cur = copy.deepcopy(func)
        for bit, label, run in steps:
            enabled = bool(combo & bit)
            if not enabled:
                rows.append({"function": func.name, "pass": label, "enabled": False,
                             "delta": 0})
                continue
            before = len(cur.instructions)
            nxt = run(cur)
            after = len(nxt.instructions)
            fired = sum(1 for i in nxt.instructions if i.annotation) - \
                sum(1 for i in cur.instructions if i.annotation)
            rows.append({"function": func.name, "pass": label, "enabled": True,
                         "delta": after - before, "annotated": max(fired, 0)})
            cur = nxt
    # collapse to per-pass totals
    agg = {}
    for r in rows:
        k = r["pass"]
        a = agg.setdefault(k, {"pass": k, "enabled": r["enabled"], "delta": 0, "annotated": 0})
        a["enabled"] = a["enabled"] or r["enabled"]
        a["delta"] += r["delta"]
        a["annotated"] += r.get("annotated", 0)
    order = ["Constant Folding", "Common Subexpr. Elim.", "Loop Unrolling",
             "Loop-Invariant Code Motion", "Strength Reduction", "Dead Code Elimination"]
    return [agg[k] for k in order if k in agg]


def _time_build(c_src: str, tag: str, opt_flag: str, runs: int, expect=None):
    cr = compile_c(c_src, tag=tag, extra_flags=[opt_flag] if opt_flag else None)
    if not cr.ok:
        return {"ok": False, "error": cr.stderr}
    try:
        tr = measure_execution_time(cr.binary_path, expected_exit_code=expect,
                                    runs=runs, warmup=max(1, runs // 4), timeout=25.0)
    except RuntimeError as e:
        cleanup(cr.c_path, cr.binary_path)
        return {"ok": False, "error": str(e)}
    cleanup(cr.c_path, cr.binary_path)
    return {"ok": True, "median_ms": round(tr.median_ms, 2),
            "min_ms": round(tr.min_ms, 2), "exit_code": tr.exit_code}


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/api/examples")
def examples():
    return jsonify({"examples": EXAMPLES,
                    "model_loaded": _MODEL is not None,
                    "model_error": _MODEL_ERR})


@app.post("/api/compile")
def compile_endpoint():
    data = request.get_json(force=True) or {}
    source = data.get("source", "")
    runs = int(data.get("runs", 7))
    runs = max(3, min(runs, 15))
    t0 = time.time()

    try:
        ast, tac = _frontend(source)
    except MiniCError as e:
        return jsonify({"ok": False, "stage": "frontend", "error": str(e)})
    except Exception as e:  # noqa: BLE001
        return jsonify({"ok": False, "stage": "frontend",
                        "error": f"{type(e).__name__}: {e}\n{traceback.format_exc()}"})

    feats = all_features(ast, tac)

    # recommend
    strategy = margin = None
    if _MODEL is not None:
        combo, pred, _names = recommend_combo(feats, _MODEL)
        strategy = _MODEL.metadata.get("strategy")
        margin = _MODEL.metadata.get("margin")
    else:
        combo, pred = NUM_COMBOS - 1, None  # fall back to "all passes"

    base_c = CEmitter().emit(optimize_program(tac, 0))
    opt_c = CEmitter().emit(optimize_program(tac, combo))

    baseline = _time_build(base_c, "base", "-O0", runs)
    if not baseline["ok"]:
        return jsonify({"ok": False, "stage": "baseline compile/run", "error": baseline["error"]})
    exit_code = baseline["exit_code"]

    optimized = _time_build(opt_c, "opt", "-O0", runs, expect=exit_code)
    o2 = _time_build(base_c, "o2", "-O2", runs, expect=exit_code)

    resp = {
        "ok": True,
        "elapsed_s": round(time.time() - t0, 1),
        "return_value": exit_code,
        "outputs_match": optimized.get("ok") and optimized.get("exit_code") == exit_code,
        "combo": combo,
        "passes": get_pass_names(combo),
        "pass_abbrs": get_pass_abbrs(combo),
        "predicted_speedup": round(pred, 3) if pred is not None else None,
        "model_loaded": _MODEL is not None,
        "strategy": strategy,
        "abstain_margin": round(1 + margin, 2) if margin else None,
        "abstained": bool(strategy == "margin" and combo == 0),
        "features": feats,
        "baseline": baseline,
        "optimized": optimized,
        "o2": o2,
        "activity": _pass_activity(tac, combo),
        "tac_before": IRPrinter.format_program(optimize_program(tac, 0)),
        "tac_after": IRPrinter.format_program(optimize_program(tac, combo)),
    }
    if optimized.get("ok"):
        resp["speedup"] = round(baseline["median_ms"] / optimized["median_ms"], 3)
    if o2.get("ok"):
        resp["o2_speedup"] = round(baseline["median_ms"] / o2["median_ms"], 3)
    return jsonify(resp)


def main():
    port = int(os.environ.get("PORT", "5005"))
    url = f"http://127.0.0.1:{port}"
    print(f"MiniC Playground -> {url}")
    if _MODEL is None:
        print(f"  (no trained model at {MODEL_PATH}; falling back to 'all passes'."
              f"  run  python run_experiment.py  to train one)")
    try:
        import webbrowser
        webbrowser.open(url)
    except Exception:
        pass
    app.run(host="127.0.0.1", port=port, debug=False)


if __name__ == "__main__":
    main()
