from . import _run, PY_SRC, PY

PY_CMDS = [
    ["isort", "-rc"],
    ["black"],
    ["flake8"],
    ["pylint"],
]


if __name__ == "__main__":
    [
        print("\n", *cmd, pkg.name, "\n--\n", _run([PY, "-m", *cmd, "src"], cwd=str(pkg)))
        for cmd in PY_CMDS
        for pkg in PY_SRC.glob("wxyz_*")
    ]
