import subprocess
import sys

from . import PY_SRC, _run, PY, DIST


if __name__ == "__main__":
    _run([
        PY, "-m", "pip", "install", *(DIST / "bdist_wheel").glob("*.whl")
    ])
