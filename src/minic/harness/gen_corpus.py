"""Parametric MiniC benchmark generator.

Produces many small programs -- single-pattern *and* composite (several patterns
as separate functions with different iteration weights, so the runtime-dominant
part, and therefore the best pass combo, varies).  Everything is deterministic
and normalised to a 0..250 return value.

    python -m src.minic.harness.gen_corpus --out benchmarks/generated --n 260
"""
import argparse
import os
import random
from typing import Callable, Dict, List, Tuple

# --- pattern bodies ---------------------------------------------------------
# Each returns (helper_functions_text, loop_body_text) for `int part(int reps)`,
# where the body updates `acc` and reads `i` (the loop counter, step 1).

def _p_licm(rng) -> Tuple[str, str]:
    a, b, c = rng.randint(11, 199), rng.randint(11, 199), rng.randint(11, 199)
    k = rng.randint(3, 6)
    terms = rng.sample(
        [f"{a} * {b}", f"{c} * {a}", f"{a} * {a}", f"{b} * {b}", f"{c} * {c}",
         f"{a} * {b} * {c}", f"{a} * {c}", f"{b} * {c} * {a}"], k)
    return "", "acc = acc + " + " + ".join(terms) + ";"


def _p_cse(rng) -> Tuple[str, str]:
    m = rng.choice([7919, 6997, 4093, 10007, 3571])
    mul = rng.randint(13, 97)
    reps = rng.randint(3, 5)
    e = f"(x * {mul}) % {m}"
    lines = [f"int c{j} = {e};" for j in range(reps)]
    lines.append("acc = acc + " + " + ".join(f"c{j}" for j in range(reps)) + ";")
    lines.append("x = x + 3;")
    return "", "\n        ".join(lines)


def _p_sr(rng) -> Tuple[str, str]:
    ks = rng.sample([3, 5, 7, 11, 13, 17, 23, 31, 57], rng.randint(1, 3))
    return "", "acc = acc + " + " + ".join(f"i * {k}" for k in ks) + f" + {rng.randint(1, 9)};"


def _p_cf(rng) -> Tuple[str, str]:
    # single-assignment constants flow into the loop body -> constant folding
    terms = ["p * q", "p * p", "q * r", "p * q * r", "r * r * p", "q * p * q"]
    rng.shuffle(terms)
    body = (f"int p = {rng.randint(3, 40)};\n        int q = {rng.randint(3, 40)};\n"
            f"        int r = {rng.randint(3, 40)};\n        "
            "acc = acc + " + " + ".join(terms[:rng.randint(3, 5)])
            + " + (i - (i / 7) * 7);")
    return "", body


def _p_div(rng) -> Tuple[str, str]:
    d1, d2 = rng.randint(40000, 99999), rng.randint(40000, 99999)
    N1, N2 = rng.randint(10 ** 8, 2 * 10 ** 9), rng.randint(10 ** 8, 2 * 10 ** 9)
    return "", (f"int u = {d1};\n        int v = {d2};\n        "
                f"acc = acc + {N1} / u + {N2} / v + i / (u - (u / 100) * 100 + 1);")


def _p_struct(rng) -> Tuple[str, str]:
    x0, y0 = rng.randint(2, 40), rng.randint(2, 40)
    x1, y1 = rng.randint(50, 99), rng.randint(50, 99)
    helper = ("struct __Box { int x0; int y0; int x1; int y1; };\n")
    body = (f"struct __Box bb;\n        bb.x0 = {x0}; bb.y0 = {y0}; "
            f"bb.x1 = {x1}; bb.y1 = {y1};\n        "
            "int w = bb.x1 - bb.x0;\n        int h = bb.y1 - bb.y0;\n        "
            "acc = acc + w * h + w * w + h * h + w * h * i;")
    return helper, body


def _p_unroll(rng) -> Tuple[str, str]:
    k = rng.randint(2, 9)
    return "", f"acc = acc + i * {k} - (i - (i / {rng.randint(3,9)}) * {rng.randint(3,9)});"


def _p_neutral(rng) -> Tuple[str, str]:
    # data-dependent, little for the passes to remove
    return "", ("int t = acc - (acc / 100003) * 100003;\n        "
                "acc = acc + t * 3 + i - (t - (t / 7) * 7);")


PATTERNS: Dict[str, Callable] = {
    "licm": _p_licm, "cse": _p_cse, "sr": _p_sr, "cf": _p_cf, "div": _p_div,
    "struct": _p_struct, "unroll": _p_unroll, "neutral": _p_neutral,
}
_NEEDS_X = {"cse"}


def _emit_part(idx: int, kind: str, rng) -> Tuple[str, str]:
    helper, body = PATTERNS[kind](rng)
    xdecl = "int x = 1;\n    " if kind in _NEEDS_X else ""
    fn = (f"int part{idx}(int reps) {{\n"
          f"    int acc = 0;\n    {xdecl}int i = 0;\n"
          f"    while (i < reps) {{\n        {body}\n        i = i + 1;\n    }}\n"
          f"    return acc;\n}}\n")
    return helper, fn


def generate(n: int, seed: int = 7) -> List[Tuple[str, str]]:
    """Return [(filename, source)]."""
    rng = random.Random(seed)
    kinds = list(PATTERNS)
    out: List[Tuple[str, str]] = []

    # ~40% single-pattern (parameter sweeps), ~60% composites
    # cost-per-iteration is very roughly: div ~4x, cse ~3x, others ~1x
    _weight_div = {"div": 4, "cse": 3, "struct": 2}

    n_single = int(n * 0.4)
    for j in range(n_single):
        kind = kinds[j % len(kinds)]
        base = rng.choice([10, 16, 24, 36, 52, 80]) * 1_000_000
        reps = max(3_000_000, base // _weight_div.get(kind, 1))
        helper, fn = _emit_part(0, kind, rng)
        src = (f"// generated: single pattern '{kind}'\n{helper}{fn}\n"
               f"int main() {{\n    int s = part0({reps});\n"
               f"    return ((s % 251) + 251) % 251;\n}}\n")
        out.append((f"g_{kind}_{j:03d}.mc", src))

    for j in range(n - n_single):
        m = rng.randint(2, 4)
        chosen = [rng.choice(kinds) for _ in range(m)]
        helpers, fns, calls = [], [], []
        for idx, kind in enumerate(chosen):
            h, fn = _emit_part(idx, kind, rng)
            if h and h not in helpers:
                helpers.append(h)
            fns.append(fn)
            w = rng.choice([8, 16, 32, 60, 110]) * 100_000
            w = max(700_000, w // _weight_div.get(kind, 1))
            calls.append(f"    s = s + part{idx}({w});")
        src = ("// generated: composite " + "+".join(chosen) + "\n"
               + "".join(helpers) + "\n" + "\n".join(fns) + "\n"
               + "int main() {\n    int s = 0;\n" + "\n".join(calls)
               + "\n    return ((s % 251) + 251) % 251;\n}\n")
        out.append((f"g_comp_{j:03d}_{'-'.join(chosen)}.mc", src))

    return out


def _main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="benchmarks/generated")
    p.add_argument("--n", type=int, default=240)
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--validate", action="store_true",
                   help="parse/lower each and drop any that fail")
    args = p.parse_args(argv)
    os.makedirs(args.out, exist_ok=True)

    progs = generate(args.n, args.seed)
    kept = 0
    if args.validate:
        from .sweeper import frontend
        good = []
        for fn, src in progs:
            try:
                frontend(src)
                good.append((fn, src))
            except Exception as e:  # noqa: BLE001
                print(f"  drop {fn}: {e}")
        progs = good

    for fn, src in progs:
        with open(os.path.join(args.out, fn), "w", newline="\n") as fh:
            fh.write(src)
        kept += 1
    print(f"wrote {kept} programs -> {args.out}")


if __name__ == "__main__":
    _main()
