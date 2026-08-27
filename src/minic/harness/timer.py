"""High-resolution wall-clock timing of a compiled benchmark binary."""
import subprocess
import time
from dataclasses import dataclass
from statistics import median
from typing import List, Optional


@dataclass
class TimingResult:
    median_ms: float
    mean_ms: float
    min_ms: float
    stdev_ms: float
    exit_code: int
    samples_ms: List[float]
    runs: int
    warmup: int


def measure_execution_time(bin_path: str,
                           expected_exit_code: Optional[int] = None,
                           runs: int = 20, warmup: int = 3,
                           timeout: float = 120.0) -> TimingResult:
    """Run ``bin_path`` ``runs`` times, drop the first ``warmup``, return stats.

    Raises ``RuntimeError`` if any run's exit code disagrees with
    ``expected_exit_code`` -- a timing sample from a miscompiled binary is
    worthless.
    """
    samples: List[float] = []
    exit_code = 0
    for i in range(runs):
        t0 = time.perf_counter_ns()
        cp = subprocess.run([bin_path], capture_output=True, timeout=timeout)
        t1 = time.perf_counter_ns()
        exit_code = cp.returncode
        if expected_exit_code is not None and exit_code != expected_exit_code:
            raise RuntimeError(
                f"{bin_path}: exit {exit_code}, expected {expected_exit_code}")
        if i >= warmup:
            samples.append((t1 - t0) / 1_000_000.0)

    if not samples:  # warmup >= runs; fall back to the last run
        samples = [(t1 - t0) / 1_000_000.0]

    m = sum(samples) / len(samples)
    var = sum((s - m) ** 2 for s in samples) / len(samples)
    return TimingResult(
        median_ms=median(samples),
        mean_ms=m,
        min_ms=min(samples),
        stdev_ms=var ** 0.5,
        exit_code=exit_code,
        samples_ms=samples,
        runs=runs,
        warmup=warmup,
    )
