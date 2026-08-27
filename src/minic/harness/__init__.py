"""Timing harness + automated 64-combo sweep (Person C)."""
from .compiler import compile_c, cleanup, CompileResult
from .timer import measure_execution_time, TimingResult
from .sweeper import sweep, discover_benchmarks, frontend
from .report import summarize, render_markdown

__all__ = [
    "compile_c", "cleanup", "CompileResult",
    "measure_execution_time", "TimingResult",
    "sweep", "discover_benchmarks", "frontend",
    "summarize", "render_markdown",
]
