""" wxyz top-level automation
"""
import site
import sys
from pathlib import Path

DODO = Path(__file__)
ROOT = DODO.parent
CI = ROOT / "ci"
SRC = ROOT / "src"
TS_SRC = SRC / "ts"
PY_SRC = SRC / "py"
PY_SETUP = [*PY_SRC.glob("*/setup.py")]
SITE_PKGS = Path(site.getsitepackages()[0])

PY_LINT_CMDS = [
    ["isort", "-rc"],
    ["black", "--quiet"],
    ["flake8"],
    ["pylint"],
]

DOIT_CONFIG = {
    "backend": "sqlite3",
}


def task_setup():
    """ make all the setups
    """
    yield dict(
        basename="js_setup",
        doc="☕ setup",
        file_dep=[ROOT / "yarn.lock"],
        targets=[ROOT / "node_modules" / ".yarn-integrity"],
        actions=[["jlpm", "--prefer-offline"], ["jlpm", "lerna", "bootstrap"]],
    )

    for setup_py in PY_SETUP:
        pkg = setup_py.parent

        yield dict(
            basename=f"py_setup_{pkg.name}",
            doc=f"🐍 setup {pkg.name}",
            file_dep=[setup_py, pkg / "setup.cfg"],
            targets=[SITE_PKGS / f"{pkg.name}.egg-link".replace("_", "-")],
            actions=[
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "-e",
                    str(pkg),
                    "--ignore-installed",
                    "--no-deps",
                ]
            ],
        )


def task_lint():
    """ make all the linters
    """
    yield dict(
        basename="lint_prettier",
        doc="☕ lint prettier",
        file_dep=[
            *ROOT.glob("*.yml"),
            *ROOT.glob("*.json"),
            *ROOT.glob("*.md"),
            *TS_SRC.rglob("*.ts"),
            *TS_SRC.rglob("*.css"),
            *TS_SRC.rglob("*.json"),
            *TS_SRC.rglob("*.yml"),
            *TS_SRC.rglob("*.md"),
            *PY_SRC.rglob("*.md"),
        ],
        actions=[["jlpm", "lint"]],
    )

    groups = {
        setup_py.parent.name: sorted(setup_py.parent.rglob("*.py"))
        for setup_py in PY_SETUP
    }

    groups["misc"] = [DODO]

    for label, files in groups.items():
        yield dict(
            basename=f"lint_{label}",
            doc=f"🐍 lint {label}",
            file_dep=files,
            actions=[cmd + files for cmd in PY_LINT_CMDS],
        )
