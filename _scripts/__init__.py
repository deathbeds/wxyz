from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).parent
ROOT = HERE.parent
SRC = ROOT / "src"

PY = sys.executable

def _run(args, **kwargs):
    return subprocess.check_call(list(map(str, args)), **kwargs)
