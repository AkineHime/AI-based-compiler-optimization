"""Parametric MiniC benchmark generator.

Produces many small programs -- single-pattern *and* composite (several patterns
as separate functions with different iteration weights, so the runtime-dominant
part, and therefore the best pass combo, varies).  Everything is deterministic
and normalised to a 0..250 return value.

Writes ``<out>/_manifest.csv`` (``program_id,pattern``) so the sweeper can label
each row with its optimization pattern for the per-category model comparison.

    python -m src.minic.harness.gen_corpus --out benchmarks/generated --n 870 --validate
"""
import argparse
import os
import random
from typing import Callable, Dict, List, Tuple

# --- pattern bodies -------------------------------------------------------------
# Each takes (rng, idx) and returns (helper_functions_text, loop_body_text) for
# `int partN(int reps)`; the body updates `acc` and may read `i` (loop counter).


def _p_licm(rng, idx) -> Tuple[str, str]:
    a, b, c = rng.randint(11, 199), rng.randint(11, 199), rng.randint(11, 199)
    k = rng.randint(3, 6)
    terms = rng.sample(
        [f"{a} * {b}", f"{c} * {a}", f"{a} * {a}", f"{b} * {b}", f"{c} * {c}",
         f"{a} * {b} * {c}", f"{a} * {c}", f"{b} * {c} * {a}"], k)
    return "", "acc = acc + " + " + ".join(terms) + ";"


def _p_cse(rng, idx) -> Tuple[str, str]:
    m = rng.choice([7919, 6997, 4093, 10007, 3571])
    mul = rng.randint(13, 97)
    reps = rng.randint(3, 5)
    e = f"(x * {mul}) % {m}"
    lines = [f"int c{j} = {e};" for j in range(reps)]
    lines.append("acc = acc + " + " + ".join(f"c{j}" for j in range(reps)) + ";")
    lines.append("x = x + 3;")
    return "", "\n        ".join(lines)


def _p_sr(rng, idx) -> Tuple[str, str]:
    ks = rng.sample([3, 5, 7, 11, 13, 17, 23, 31, 57], rng.randint(1, 3))
    return "", "acc = acc + " + " + ".join(f"i * {k}" for k in ks) + f" + {rng.randint(1, 9)};"


def _p_cf(rng, idx) -> Tuple[str, str]:
    terms = ["p * q", "p * p", "q * r", "p * q * r", "r * r * p", "q * p * q"]
    rng.shuffle(terms)
    body = (f"int p = {rng.randint(3, 40)};\n        int q = {rng.randint(3, 40)};\n"
            f"        int r = {rng.randint(3, 40)};\n        "
            "acc = acc + " + " + ".join(terms[:rng.randint(3, 5)])
            + " + (i - (i / 7) * 7);")
    return "", body


def _p_div(rng, idx) -> Tuple[str, str]:
    d1, d2 = rng.randint(40000, 99999), rng.randint(40000, 99999)
    N1, N2 = rng.randint(10 ** 8, 2 * 10 ** 9), rng.randint(10 ** 8, 2 * 10 ** 9)
    return "", (f"int u = {d1};\n        int v = {d2};\n        "
                f"acc = acc + {N1} / u + {N2} / v + i / (u - (u / 100) * 100 + 1);")


def _p_struct(rng, idx) -> Tuple[str, str]:
    x0, y0 = rng.randint(2, 40), rng.randint(2, 40)
    x1, y1 = rng.randint(50, 99), rng.randint(50, 99)
    helper = "struct __Box { int x0; int y0; int x1; int y1; };\n"
    body = (f"struct __Box bb;\n        bb.x0 = {x0}; bb.y0 = {y0}; "
            f"bb.x1 = {x1}; bb.y1 = {y1};\n        "
            "int w = bb.x1 - bb.x0;\n        int h = bb.y1 - bb.y0;\n        "
            "acc = acc + w * h + w * w + h * h + w * h * i;")
    return helper, body


def _p_unroll(rng, idx) -> Tuple[str, str]:
    k = rng.randint(2, 9)
    return "", f"acc = acc + i * {k} - (i - (i / {rng.randint(3,9)}) * {rng.randint(3,9)});"


def _p_neutral(rng, idx) -> Tuple[str, str]:
    return "", ("int t = acc - (acc / 100003) * 100003;\n        "
                "acc = acc + t * 3 + i - (t - (t / 7) * 7);")


def _p_branch(rng, idx) -> Tuple[str, str]:
    k1, k2, k3, k4 = (rng.randint(3, 40) for _ in range(4))
    md = rng.choice([2, 3, 4])
    return "", (f"if (i - (i / {md}) * {md} == 0) {{\n"
                f"            acc = acc + i * {k1} + {k2} * {k3};\n"
                f"        }} else {{\n"
                f"            acc = acc + i * {k4} - (i - (i / 5) * 5);\n"
                f"        }}")


def _p_nested(rng, idx) -> Tuple[str, str]:
    cap = rng.choice([6, 10, 16, 24])
    k1, k2 = rng.randint(2, 30), rng.randint(2, 30)
    return "", (f"int j = 0;\n        int inner = 0;\n"
                f"        while (j < {cap}) {{\n"
                f"            inner = inner + j * {k1} + i * {k2};\n"
                f"            j = j + 1;\n"
                f"        }}\n        acc = acc + inner;")


def _p_recur(rng, idx) -> Tuple[str, str]:
    k = rng.randint(1, 7)
    depth = rng.choice([60, 100, 160, 240])
    helper = (f"int rec{idx}(int n) {{\n"
              f"    if (n < 2) {{ return n; }}\n"
              f"    return rec{idx}(n - 1) + {k};\n}}\n")
    return helper, f"acc = acc + rec{idx}({depth});"


PATTERNS: Dict[str, Callable] = {
    "licm": _p_licm, "cse": _p_cse, "sr": _p_sr, "cf": _p_cf, "div": _p_div,
    "struct": _p_struct, "unroll": _p_unroll, "neutral": _p_neutral,
    "branch": _p_branch, "nested": _p_nested, "recur": _p_recur,
}
_NEEDS_X = {"cse"}


# rough cost per iteration relative to a plain `acc += ...`; tuned so combo-0
# runtime lands ~25-70 ms (single) / ~15-40 ms (composite part).
_COST = {"div": 5, "cse": 4, "cf": 3, "struct": 3, "neutral": 3, "branch": 3,
         "unroll": 2, "nested": 26, "recur": 1500}


def _single_reps(kind: str, rng) -> int:
    base = rng.choice([3, 5, 8, 12, 18]) * 1_000_000
    floor = {"nested": 120_000, "recur": 10_000}.get(kind, 1_500_000)
    return max(floor, base // _COST.get(kind, 1))


def _comp_reps(kind: str, rng) -> int:
    w = rng.choice([3, 6, 11, 20, 34]) * 100_000
    floor = {"nested": 40_000, "recur": 4_000}.get(kind, 300_000)
    return max(floor, w // _COST.get(kind, 1))


def _emit_part(idx: int, kind: str, rng, use_for: bool) -> Tuple[str, str]:
    helper, body = PATTERNS[kind](rng, idx)
    xdecl = "    int x = 1;\n" if kind in _NEEDS_X else ""
    if use_for and kind != "nested":   # keep the nested pattern's own inner loop tidy
        loop = (f"    for (int i = 0; i < reps; i = i + 1) {{\n"
                f"        {body}\n    }}\n")
    else:
        loop = (f"    int i = 0;\n    while (i < reps) {{\n"
                f"        {body}\n        i = i + 1;\n    }}\n")
    fn = (f"int part{idx}(int reps) {{\n    int acc = 0;\n{xdecl}{loop}"
          f"    return acc;\n}}\n")
    return helper, fn


def generate(n: int, seed: int = 7) -> List[Tuple[str, str, str]]:
    """Return [(filename, source, pattern)] -- pattern is the kind, or 'composite'."""
    rng = random.Random(seed)
    kinds = list(PATTERNS)
    out: List[Tuple[str, str, str]] = []

    n_single = int(n * 0.4)
    for j in range(n_single):
        kind = kinds[j % len(kinds)]
        reps = _single_reps(kind, rng)
        helper, fn = _emit_part(0, kind, rng, use_for=rng.random() < 0.4)
        src = (f"// generated: single pattern '{kind}'\n{helper}{fn}\n"
               f"int main() {{\n    int s = part0({reps});\n"
               f"    return ((s % 251) + 251) % 251;\n}}\n")
        out.append((f"g_{kind}_{j:03d}.mc", src, kind))

    for j in range(n - n_single):
        m = rng.randint(2, 4)
        chosen = [rng.choice(kinds) for _ in range(m)]
        helpers, fns, calls = [], [], []
        use_for = rng.random() < 0.4
        for idx, kind in enumerate(chosen):
            h, fn = _emit_part(idx, kind, rng, use_for)
            if h and h not in helpers:
                helpers.append(h)
            fns.append(fn)
            calls.append(f"    s = s + part{idx}({_comp_reps(kind, rng)});")
        src = ("// generated: composite " + "+".join(chosen) + "\n"
               + "".join(helpers) + "\n" + "\n".join(fns) + "\n"
               + "int main() {\n    int s = 0;\n" + "\n".join(calls)
               + "\n    return ((s % 251) + 251) % 251;\n}\n")
        out.append((f"g_comp_{j:03d}_{'-'.join(chosen)}.mc", src, "composite"))

    return out


def _main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="benchmarks/generated")
    p.add_argument("--n", type=int, default=870)
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--validate", action="store_true",
                   help="parse/lower each and drop any that fail")
    args = p.parse_args(argv)
    os.makedirs(args.out, exist_ok=True)

    progs = generate(args.n, args.seed)
    if args.validate:
        from .sweeper import frontend
        good = []
        for fn, src, pat in progs:
            try:
                frontend(src)
                good.append((fn, src, pat))
            except Exception as e:  # noqa: BLE001
                print(f"  drop {fn}: {e}")
        progs = good

    for fn, src, _pat in progs:
        with open(os.path.join(args.out, fn), "w", newline="\n") as fh:
            fh.write(src)
    with open(os.path.join(args.out, "_manifest.csv"), "w", newline="\n", encoding="utf-8") as fh:
        fh.write("program_id,pattern\n")
        for fn, _src, pat in progs:
            fh.write(f"{os.path.splitext(fn)[0]},{pat}\n")

    from collections import Counter
    dist = Counter(pat for _fn, _src, pat in progs)
    print(f"wrote {len(progs)} programs + _manifest.csv -> {args.out}")
    print("  " + "  ".join(f"{k}:{v}" for k, v in sorted(dist.items())))


if __name__ == "__main__":
    _main()
