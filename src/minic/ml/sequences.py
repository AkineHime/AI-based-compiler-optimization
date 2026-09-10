"""Serialise a program's unoptimised (combo-0) TAC into an integer token
sequence for the sequence models (1D-CNN, GRU).

Each instruction becomes 4 tokens: its opcode, then the *kind* of its dst /
src1 / src2 operand (temp / var / const / label / none).  Operand names and
literal values are deliberately dropped -- the model sees the shape of the
computation, not its constants.  Functions are separated by <func>.
"""
import os
from typing import Dict, List

from ..ir.tac import Opcode, Temp, Var, Constant, Label

_SPECIAL = ["<pad>", "<func>", "<eos>"]
_OPS = [op.name for op in Opcode]
_KINDS = ["K_NONE", "K_TEMP", "K_VAR", "K_CONST", "K_LABEL", "K_OTHER"]
VOCAB: List[str] = _SPECIAL + _OPS + _KINDS
STOI: Dict[str, int] = {t: i for i, t in enumerate(VOCAB)}
PAD = STOI["<pad>"]
VOCAB_SIZE = len(VOCAB)
MAX_LEN = 640  # corpus p99 of the untrimmed length is ~625


def _kind(operand) -> str:
    if operand is None:
        return "K_NONE"
    if isinstance(operand, Temp):
        return "K_TEMP"
    if isinstance(operand, Var):
        return "K_VAR"
    if isinstance(operand, Constant):
        return "K_CONST"
    if isinstance(operand, Label):
        return "K_LABEL"
    return "K_OTHER"  # e.g. CALL's string func-name / int arg-count


def tokenize_tac(tac_program, max_len: int = MAX_LEN) -> List[int]:
    toks: List[int] = []
    for fn in tac_program.functions:
        toks.append(STOI["<func>"])
        for ins in fn.instructions:
            if ins.opcode is Opcode.COMMENT:
                continue
            toks.append(STOI[ins.opcode.name])
            toks.append(STOI[_kind(ins.dst)])
            toks.append(STOI[_kind(ins.src1)])
            toks.append(STOI[_kind(ins.src2)])
        toks.append(STOI["<eos>"])
    return toks[:max_len]


def export_sequences(bench_root: str = "benchmarks",
                     out_path: str = "data/tac_sequences.npz",
                     max_len: int = MAX_LEN) -> str:
    import numpy as np
    from ..harness.sweeper import frontend, discover_benchmarks

    pids: List[str] = []
    rows: List[List[int]] = []
    lengths: List[int] = []
    capped = 0
    for path in discover_benchmarks(bench_root):
        pid = os.path.splitext(os.path.basename(path))[0]
        try:
            _ast, tac = frontend(open(path, encoding="utf-8").read())
        except Exception:  # noqa: BLE001 -- a broken benchmark just gets skipped
            continue
        toks = tokenize_tac(tac, max_len)
        capped += len(toks) >= max_len
        pids.append(pid)
        lengths.append(len(toks))
        rows.append(toks + [PAD] * (max_len - len(toks)))

    mat = np.asarray(rows, dtype=np.int16)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    np.savez_compressed(out_path, pids=np.asarray(pids), tokens=mat,
                        lengths=np.asarray(lengths, dtype=np.int32),
                        vocab=np.asarray(VOCAB))
    print(f"wrote {len(pids)} sequences -> {out_path}  "
          f"(max_len={max_len}, {capped} capped, "
          f"median len {int(np.median(lengths))}, p95 {int(np.percentile(lengths, 95))})")
    return out_path


def load_sequences(path: str = "data/tac_sequences.npz"):
    import numpy as np
    d = np.load(path, allow_pickle=True)
    pids = [str(p) for p in d["pids"]]
    return {
        "by_pid": {pid: d["tokens"][i] for i, pid in enumerate(pids)},
        "lengths": {pid: int(d["lengths"][i]) for i, pid in enumerate(pids)},
        "vocab": [str(v) for v in d["vocab"]],
    }


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description="Export TAC token sequences for the sequence models")
    p.add_argument("--bench-root", default="benchmarks")
    p.add_argument("--out", default="data/tac_sequences.npz")
    p.add_argument("--max-len", type=int, default=MAX_LEN)
    a = p.parse_args()
    export_sequences(a.bench_root, a.out, a.max_len)
