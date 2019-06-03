import sys

from . import PY, LAB, _run


if __name__ == "__main__":
    _run(["jupyter", "labextension", *sys.argv[1:], "--app-dir", LAB])
