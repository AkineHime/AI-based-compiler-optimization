"""One entry point for everything in this project.

    python minic.py check                         is my setup OK? (Python packages, gcc, data)
    python minic.py compile  FILE.mc [options]    compile a MiniC file, show TAC / C / features, run it
    python minic.py recommend FILE.mc [--verify]  ask the ML model which passes to enable (and time it)
    python minic.py benchmark FILE.mc             time each optimization pass on a file
    python minic.py playground                    open the browser playground (http://127.0.0.1:5005)
    python minic.py results                       rebuild the visual results page and open it
    python minic.py analyze                       rewrite PERF_ANALYSIS.md from the dataset
    python minic.py experiment                    retrain + re-evaluate the model (~4 min)
    python minic.py experiment --full             re-time all 57,600 builds first (~3.5 h)
    python minic.py test [--quick]                run the test suite

Run `python minic.py COMMAND --help` for each command's options.
"""
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)              # every command uses paths relative to the repo root
sys.path.insert(0, ROOT)

for _s in (sys.stdout, sys.stderr):  # box-drawing glyphs on the Windows console
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

COMMANDS = {}


def command(name, summary):
    def deco(fn):
        COMMANDS[name] = (fn, summary)
        return fn
    return deco


@command("check", "check Python packages, gcc and the dataset")
def cmd_check(args):
    import importlib
    import shutil
    ok = True

    def line(good, what, hint=""):
        nonlocal ok
        ok &= good
        print(f"  {'OK  ' if good else 'FAIL'}  {what}" + (f"\n          -> {hint}" if hint and not good else ""))

    print("MiniC setup check\n")
    line(sys.version_info >= (3, 9), f"Python {sys.version.split()[0]} (need 3.9+)",
         "install Python 3.9 or newer")
    from importlib.metadata import version, PackageNotFoundError
    for mod, pkg in (("numpy", "numpy"), ("sklearn", "scikit-learn"), ("pandas", "pandas"),
                     ("flask", "flask"), ("matplotlib", "matplotlib"), ("pytest", "pytest")):
        try:
            importlib.import_module(mod)
            try:
                ver = version(pkg)
            except PackageNotFoundError:
                ver = ""
            line(True, f"{pkg} {ver}")
        except ImportError:
            line(False, f"{pkg} missing", "pip install -r requirements.txt")
    gcc = shutil.which("gcc")
    if gcc:
        import subprocess
        ver = subprocess.run([gcc, "--version"], capture_output=True, text=True).stdout.splitlines()
        line(True, f"gcc: {ver[0] if ver else gcc}")
    else:
        from src.minic.harness.compiler import GCC_MISSING
        line(False, "gcc not on PATH", GCC_MISSING.split("\n", 1)[1].strip())
    csv = os.path.join("data", "benchmark_dataset.csv")
    line(os.path.exists(csv), f"dataset {csv}", "git checkout data/benchmark_dataset.csv")
    model = os.path.join("data", "trained_model.pkl")
    print(f"  {'OK  ' if os.path.exists(model) else 'INFO'}  model {model}"
          + ("" if os.path.exists(model) else " (trained automatically on first use, ~15 s)"))
    try:
        import torch  # noqa: F401
        print("  OK    torch (optional, for --compare-models)")
    except ImportError:
        print("  INFO  torch not installed (optional: only `experiment --compare-models` needs it)")

    if ok and gcc:
        print("\nsmoke test: compile + run canonical_example.mc with all passes ...")
        from src.minic.driver import main as driver_main
        driver_main(["canonical_example.mc", "--optimize", "63", "--run"])
    print("\nAll good." if ok else "\nFix the FAIL lines above, then run this again.")
    return 0 if ok else 1


@command("compile", "compile a MiniC file (TAC / C / features / run)")
def cmd_compile(args):
    from src.minic.driver import main
    return main(args)


@command("recommend", "ML-recommended passes for a file (--verify to time it)")
def cmd_recommend(args):
    from demo.cli import main
    return main(["recommend"] + args)


@command("benchmark", "time each optimization pass on a file")
def cmd_benchmark(args):
    from demo.cli import main
    return main(["benchmark"] + args)


@command("playground", "browser playground at http://127.0.0.1:5005")
def cmd_playground(args):
    import argparse
    p = argparse.ArgumentParser(prog="minic.py playground")
    p.add_argument("--port", type=int, default=None, help="default: $PORT, else 5005")
    a = p.parse_args(args)
    if a.port is not None:
        os.environ["PORT"] = str(a.port)
    from demo.app import main
    return main()


@command("results", "rebuild docs/results.html and open it")
def cmd_results(args):
    import argparse
    p = argparse.ArgumentParser(prog="minic.py results",
                                description="Rebuild the results page from the dataset.")
    p.add_argument("--no-open", action="store_true", help="don't open it in the browser")
    p.add_argument("--recompute", action="store_true",
                   help="re-run the held-out ML evaluation instead of using the cache (~1 min)")
    a = p.parse_args(args)
    from src.minic.harness.gen_resultspage import build
    page = build(recompute=a.recompute)
    if not a.no_open:
        import webbrowser
        webbrowser.open("file://" + os.path.abspath(page))
    return 0


@command("analyze", "write PERF_ANALYSIS.md from the dataset")
def cmd_analyze(args):
    from src.minic.harness.perf_analysis import _main
    return _main(args)


@command("experiment", "retrain + evaluate (--full re-times every build, ~3.5 h)")
def cmd_experiment(args):
    import run_experiment
    if "--full" in args:
        args = [a for a in args if a != "--full"]
    elif "--quick" not in args and "--skip-sweep" not in args:
        args = ["--skip-sweep"] + args
    return run_experiment.main(args)


@command("test", "run the tests (--quick skips the slow 64-combo sweeps)")
def cmd_test(args):
    import pytest
    if "--quick" in args:
        args = [a for a in args if a != "--quick"] + ["-m", "not slow"]
    return pytest.main(["-q"] + args)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(__doc__.strip())
        return 0
    name, rest = argv[0], argv[1:]
    if name not in COMMANDS:
        print(f"unknown command '{name}'. Commands: {', '.join(COMMANDS)}\n"
              f"Run `python minic.py --help` for details.")
        return 2
    try:
        return COMMANDS[name][0](rest) or 0
    except KeyboardInterrupt:
        return 130
    except ModuleNotFoundError as e:
        # usually: running with a Python that doesn't have requirements.txt installed
        venv = os.path.join(ROOT, ".venv")
        print(f"\nMissing Python package: {e.name}\n"
              f"This Python ({sys.executable}) doesn't have the project's packages.\n")
        if os.path.isdir(venv) and os.path.abspath(sys.prefix) != os.path.abspath(venv):
            act = r".venv\Scripts\activate" if os.name == "nt" else "source .venv/bin/activate"
            print(f"This folder has a virtual environment. Activate it, then run the command again:\n"
                  f"    {act}\n\nor install the packages into this Python:")
        else:
            print("Install them with:")
        print("    pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(main())
