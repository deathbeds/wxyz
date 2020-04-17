""" wxyz top-level automation
"""
import site
import sys
from pathlib import Path
from subprocess import call

from doit.tools import result_dep

PY = Path(sys.executable)

DODO = Path(__file__)
ROOT = DODO.parent
DIST = ROOT / "dist"
CI = ROOT / "ci"

SRC = ROOT / "src"

TS_SRC = SRC / "ts"
PY_SRC = SRC / "py"
PY_SETUP = [*PY_SRC.glob("*/setup.py")]
SITE_PKGS = Path(site.getsitepackages()[0])

PY_LINT_CMDS = [
    ["isort", "-rc"],
    ["black", "--quiet"],
    ["flake8", "--max-line-length", "88"],
    ["pylint"],
]

DOIT_CONFIG = {
    "backend": "sqlite3",
}


def task_setup():
    """ make all the setups
    """
    yield dict(
        name="js",
        file_dep=[ROOT / "yarn.lock"],
        targets=[ROOT / "node_modules" / ".yarn-integrity"],
        actions=[["jlpm", "--prefer-offline"], ["jlpm", "lerna", "bootstrap"]],
    )

    for i, setup_py in enumerate(PY_SETUP):
        pkg = setup_py.parent

        uptodate = {}

        if i:
            uptodate["uptodate"] = [result_dep(f"setup:py_{PY_SETUP[i-1].parent.name}")]

        yield dict(
            name=f"py_{pkg.name}",
            file_dep=[setup_py, pkg / "setup.cfg"],
            targets=[SITE_PKGS / f"{pkg.name}.egg-link".replace("_", "-")],
            actions=[
                [
                    PY,
                    "-m",
                    "pip",
                    "install",
                    "-e",
                    str(pkg),
                    "--ignore-installed",
                    "--no-deps",
                ]
            ],
            **uptodate,
        )


def task_lint():
    """ make all the linters
    """
    uptodate = dict(uptodate=[result_dep("setup")])
    yield dict(
        name="prettier",
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
        **uptodate,
    )

    groups = {
        i.parent.name: [i, *sorted((i.parent / "src").rglob("*.py"))] for i in PY_SETUP
    }

    groups["misc"] = [DODO]

    for label, files in groups.items():
        actions = [cmd + files for cmd in PY_LINT_CMDS]
        yield dict(name=label, file_dep=files, actions=actions, **uptodate)


def _one_pydist(pkg, file_dep, output):
    name = f"{output}_{pkg.name}"
    args = [PY, "setup.py", output, "--dist-dir", DIST / output]
    actions = [lambda: call(args, cwd=pkg) == 0]
    return dict(
        name=name, file_dep=file_dep, actions=actions, uptodate=[result_dep("lint")]
    )


def task_pydist():
    """ build python release artifacts
    """
    for setup_py in PY_SETUP:
        pkg = setup_py.parent
        file_dep = [
            setup_py,
            pkg / "setup.cfg",
            *sorted((pkg / "src").rglob("*.py")),
        ]
        for output in ["sdist", "bdist_wheel"]:
            yield _one_pydist(pkg, file_dep, output)
