from . import _run, SRC, PY

PY_CMDS = [
    ["isort", "-rc", "src"],
    ["black", "src"],
    ["flake8", "src"],
    ["pylint", "src"],
]


if __name__ == "__main__":
    for cmd in PY_CMDS:
        for pkg in SRC.glob("wxyz_*"):
            _run([PY, "-m", *cmd], cwd=str(pkg))
