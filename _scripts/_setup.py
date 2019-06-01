import subprocess
import sys

from . import SRC, _run


if __name__ == "__main__":
    for pkg in SRC.glob("wxyz_*"):
        _run([
            sys.executable,
            "-m", "pip", "install", "-e", ".", "--ignore-installed", "--no-deps"
        ]), cwd=str(pkg))
