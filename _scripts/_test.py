import sys

from . import _run, PY_SRC, PY


def notebook_tests(extra_args=[]):
    return _run([PY, "-m", "pytest", *extra_args], cwd=PY_SRC / "wxyz_notebooks")


if __name__ == "__main__":
    sys.exit(notebook_tests(sys.argv[1:]))
