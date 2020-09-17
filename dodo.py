""" wxyz top-level automation
"""
# pylint: disable=expression-not-assigned

import shutil

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
    "verbosity": 2,
    "par_type": "thread",
}


def task_setup_ts():
    """set up typescript environment"""
    return dict(
        file_dep=[*P.TS_PACKAGE, P.ROOT_PACKAGE],
        targets=[P.YARN_INTEGRITY, P.YARN_LOCK],
        actions=[["jlpm", "--prefer-offline"], ["jlpm", "lerna", "bootstrap"]],
    )


EGG_LINKS = []


def _make_py_setup(i, setup_py):
    """make all the setups"""
    pkg = setup_py.parent

    uptodate = {}

    if i:
        uptodate["uptodate"] = [result_dep(f"setup_py_{P.PY_SETUP[i-1].parent.name}")]

    egg_link = [P.SITE_PKGS / f"{pkg.name}.egg-link".replace("_", "-")]
    EGG_LINKS.extend(egg_link)

    def _task():
        return dict(
            doc=f"{pkg.name} dev install",
            file_dep=[setup_py, pkg / "setup.cfg"],
            targets=egg_link,
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

    _task.__name__ = f"task_setup_py_{pkg.name}"

    return {_task.__name__: _task}


if P.RUNNING_IN_CI:

    def task_setup_py_ci():
        """CI: setup python packages from wheels"""
        return dict(
            file_dep=P.WHEELS,
            targets=[P.OK / "setup_py"],
            actions=[
                U.okit("setup_py", remove=True),
                [P.PY, "-m", "pip", "install", *P.WHEELS],
                [P.PY, "-m", "pip", "freeze"],
                U.okit("setup_py"),
            ],
        )


if not P.RUNNING_IN_CI:
    [
        globals().update(**_make_py_setup(i, setup_py))
        for i, setup_py in enumerate(P.PY_SETUP)
    ]

    def task_setup_py_dev():
        """setup python packages for development"""
        return dict(
            file_dep=EGG_LINKS,
            targets=[P.OK / "setup_py"],
            actions=[
                U.okit("setup_py", remove=True),
                [P.PY, "-m", "pip", "freeze"],
                U.okit("setup_py"),
            ],
        )


def task_lint_prettier():
    """use prettier to format things"""

    return dict(
        file_dep=[P.YARN_INTEGRITY, P.YARN_LOCK, *P.ALL_PRETTIER],
        targets=[P.OK / "prettier"],
        actions=[
            U.okit("prettier", remove=True),
            ["jlpm", "lint"],
            U.okit("prettier"),
        ],
    )


LINT_GROUPS = {
    i.parent.name: [i, *sorted((i.parent / "src").rglob("*.py"))] for i in P.PY_SETUP
}

LINT_GROUPS["misc"] = [P.DODO, *P.SCRIPTS.glob("*.py")]


def _make_linter(label, files):
    def _task():
        return dict(
            file_dep=[*files, *EGG_LINKS],
            actions=[cmd + files for cmd in PY_LINT_CMDS if shutil.which(cmd[0])],
        )

    _task.__name__ = f"task_lint_py_{label}"
    _task.__doc__ = f"format/lint {label}"

    return {_task.__name__: _task}


[globals().update(_make_linter(label, files)) for label, files in LINT_GROUPS.items()]


def _make_pydist(setup_py):
    """build python release artifacts"""
    pkg = setup_py.parent
    file_dep = [
        setup_py,
        pkg / "setup.cfg",
        *sorted((pkg / "src").rglob("*.py")),
    ]

    def _action(output):
        """build a single task so we can run in the cwd"""
        args = [P.PY, "setup.py", output, "--dist-dir", P.DIST / output]
        return lambda: U.call(args, cwd=pkg) == 0

    def _task():
        return dict(
            doc=f"build {pkg.name} distributions",
            file_dep=file_dep,
            actions=[_action("sdist"), _action("bdist_wheel")],
        )

    _task.__name__ = f"task_dist_py_{pkg.name}"

    return {_task.__name__: _task}


[globals().update(_make_pydist(pys)) for pys in P.PY_SETUP]


def task_ts():
    """build typescript components"""
    return dict(
        file_dep=[P.YARN_LOCK, *P.TS_PACKAGE, P.OK / "prettier"],
        targets=[*P.TS_TARBALLS],
        actions=[["jlpm", "build"]],
    )


def task_nbtest():
    """smoke test all notebooks with nbconvert"""
    return dict(
        file_dep=[*P.ALL_SRC_PY, *P.ALL_IPYNB, P.OK / "setup_py"],
        targets=[P.OK / "nbtest"],
        actions=[
            U.okit("nbtest", True),
            lambda: U.call(
                [P.PY, "-m", "pytest", "-vv"], cwd=P.PY_SRC / "wxyz_notebooks"
            )
            == 0,
            U.okit("nbtest"),
        ],
    )


JPY = [P.PY, "-m", "jupyter"]

if P.RUNNING_IN_BINDER:
    APP_DIR = ["--debug"]
else:
    APP_DIR = ["--debug", "--app-dir", P.LAB]


def task_lab_extensions():
    """set up local jupyterlab"""

    return dict(
        file_dep=[*P.TS_PACKAGE, *P.TS_TARBALLS],
        targets=[P.OK / "labextensions"],
        actions=[
            U.okit("labextensions", True),
            [
                *JPY,
                "labextension",
                "install",
                *P.ALL_LABEXTENSIONS,
                "--no-build",
                *APP_DIR,
            ],
            U.okit("labextensions"),
        ],
    )


def task_lab_build():
    """build JupyterLab web application"""

    args = [*JPY, "lab", "build", "--dev-build=False", "--debug"]

    # binder runs out of memory
    if P.RUNNING_IN_BINDER:
        args += ["--minimize=False"]
    else:
        args += ["--minimize=True"]

    return dict(
        file_dep=[P.OK / "labextensions", *P.TS_TARBALLS],
        targets=[P.OK / "lab"],
        actions=[
            U.okit("lab", True),
            args,
            U.okit("lab"),
        ],
    )


def task_binder():
    """get to a working interactive state"""
    return dict(file_dep=[P.OK / "lab", *EGG_LINKS], actions=[lambda: print("OK")])


ATEST = [P.PY, "-m", "_scripts._atest"]


def task_robot_dry_run():
    """dry run robot syntax"""

    return dict(
        file_dep=[*P.ALL_ROBOT, *P.ALL_SRC_PY, *P.ALL_TS],
        targets=[P.OK / "robot_dry_run"],
        actions=[
            U.okit("robot_dry_run", True),
            [*ATEST, "--dryrun"],
            U.okit("robot_dry_run"),
        ],
    )


def task_robot():
    """test in browser with robot framework"""

    return dict(
        file_dep=[
            *P.ALL_ROBOT,
            *P.ALL_SRC_PY,
            *P.ALL_TS,
            P.OK / "lab",
            P.OK / "robot_dry_run",
            P.OK / "nbtest",
        ],
        actions=[[*ATEST]],
    )
