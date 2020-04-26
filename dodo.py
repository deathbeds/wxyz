""" wxyz top-level automation
"""
from doit.tools import result_dep

from _scripts import _paths as P
from _scripts import _util as U

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
        name="ts",
        file_dep=[*P.TS_PACKAGE, P.ROOT_PACKAGE],
        targets=[P.YARN_INTEGRITY, P.YARN_LOCK],
        actions=[["jlpm", "--prefer-offline"], ["jlpm", "lerna", "bootstrap"]],
    )

    for i, setup_py in enumerate(P.PY_SETUP):
        pkg = setup_py.parent

        uptodate = {}

        if i:
            uptodate["uptodate"] = [
                result_dep(f"setup:py_{P.PY_SETUP[i-1].parent.name}")
            ]

        yield dict(
            name=f"py_{pkg.name}",
            file_dep=[setup_py, pkg / "setup.cfg"],
            targets=[P.SITE_PKGS / f"{pkg.name}.egg-link".replace("_", "-")],
            actions=[
                [
                    P.PY,
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
            *P.ROOT.glob("*.yml"),
            *P.ROOT.glob("*.json"),
            *P.ROOT.glob("*.md"),
            *P.TS_SRC.rglob("*.ts"),
            *P.TS_SRC.rglob("*.css"),
            *P.TS_SRC.rglob("*.json"),
            *P.TS_SRC.rglob("*.yml"),
            *P.TS_SRC.rglob("*.md"),
            *P.PY_SRC.rglob("*.md"),
        ],
        actions=[["jlpm", "lint"]],
        **uptodate,
    )

    groups = {
        i.parent.name: [i, *sorted((i.parent / "src").rglob("*.py"))]
        for i in P.PY_SETUP
    }

    groups["misc"] = [P.DODO, *P.SCRIPTS.glob("*.py")]

    for label, files in groups.items():
        actions = [cmd + files for cmd in PY_LINT_CMDS]
        yield dict(name=label, file_dep=files, actions=actions, **uptodate)


def _one_pydist(pkg, file_dep, output):
    """ build a single task so we can run in the cwd
    """
    name = f"{output}_{pkg.name}"
    args = [P.PY, "setup.py", output, "--dist-dir", P.DIST / output]
    actions = [lambda: U.call(args, cwd=pkg) == 0]
    return dict(
        name=name, file_dep=file_dep, actions=actions, uptodate=[result_dep("lint")]
    )


def task_pydist():
    """ build python release artifacts
    """
    for setup_py in P.PY_SETUP:
        pkg = setup_py.parent
        file_dep = [
            setup_py,
            pkg / "setup.cfg",
            *sorted((pkg / "src").rglob("*.py")),
        ]
        for output in ["sdist", "bdist_wheel"]:
            yield _one_pydist(pkg, file_dep, output)


def task_ts():
    """ build typescript components
    """
    return dict(
        file_dep=[P.YARN_LOCK, *P.TS_PACKAGE],
        targets=[*P.TS_TARBALLS],
        actions=[["jlpm", "build"]],
        uptodate=[result_dep("lint:prettier")],
    )
