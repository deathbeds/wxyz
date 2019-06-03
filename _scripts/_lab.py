import sys
from . import PY, LAB, _run


if __name__ == "__main__":
    _run([PY, "-m", "jupyter", "lab", *sys.argv[1:], "--no-browser", "--app-dir", LAB])
