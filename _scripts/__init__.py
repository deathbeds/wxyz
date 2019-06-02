from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).parent
ROOT = HERE.parent
SRC = ROOT / "src"
PY_SRC = SRC / "py"
TS_SRC = SRC / "ts"

PY = sys.executable

DIST = ROOT / "dist"

def _run(args, **kwargs):
    return subprocess.check_call(list(map(str, args)), **kwargs)
