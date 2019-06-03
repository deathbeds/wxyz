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
IPYNB = ROOT / "notebooks"
IPYNB_HTML = DIST / "notebooks"

TEST_OUT = DIST / "test_output"
ROBOT_OUT = TEST_OUT / "robot"
LAB = ROOT / "lab"

ATEST = ROOT / "atest"

def _run(args, **kwargs):
    return subprocess.check_call(list(map(str, args)), **kwargs)
