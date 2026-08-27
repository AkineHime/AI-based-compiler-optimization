"""Compile emitted C with ``gcc -O0`` and hand back a runnable binary path.

``-O0`` is deliberate: the whole experiment measures what *our* TAC-level
optimizer buys, so the C compiler must not do the work for us.
"""
import os
import subprocess
import tempfile
import uuid
from dataclasses import dataclass
from typing import Optional

EXE_SUFFIX = ".exe" if os.name == "nt" else ""


@dataclass
class CompileResult:
    ok: bool
    binary_path: Optional[str]
    c_path: str
    stderr: str = ""


def compile_c(c_source: str, out_dir: Optional[str] = None,
              gcc: str = "gcc", tag: str = "prog",
              extra_flags: Optional[list] = None,
              timeout: float = 60.0) -> CompileResult:
    out_dir = out_dir or tempfile.mkdtemp(prefix="minic_build_")
    os.makedirs(out_dir, exist_ok=True)
    stem = f"{tag}_{uuid.uuid4().hex[:8]}"
    c_path = os.path.join(out_dir, stem + ".c")
    bin_path = os.path.join(out_dir, stem + EXE_SUFFIX)
    with open(c_path, "w", encoding="utf-8") as fh:
        fh.write(c_source)

    cmd = [gcc, "-O0", "-std=c99", "-w", c_path, "-o", bin_path]
    if extra_flags:
        cmd[1:1] = list(extra_flags)
    try:
        cp = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return CompileResult(False, None, c_path, "gcc timed out")
    if cp.returncode != 0:
        return CompileResult(False, None, c_path, cp.stderr)
    return CompileResult(True, bin_path, c_path)


def cleanup(*paths: str) -> None:
    for p in paths:
        if p and os.path.exists(p):
            try:
                os.remove(p)
            except OSError:
                pass
