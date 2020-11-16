""" wxyz top-level automation

    this should be executed from within an environment created from
    the ci/locks/conda.*.lock appropriate for your platform. See CONTRIBUTING.md.
"""
# pylint: disable=expression-not-assigned,W0511

import shutil
import subprocess
import time

from doit.tools import PythonInteractiveAction

from _scripts import _paths as P, _util as U
from _scripts._lock import iter_matrix, make_lock_task

PY_LINT_CMDS = [
    ["isort", "-rc"],
    ["black", "--quiet"],
    ["flake8", "--max-line-length", "88"],
    ["pylint", "-sn", "-rn", f"--rcfile={P.PYLINTRC}"],
]

DOIT_CONFIG = {
    "backend": "sqlite3",
    "verbosity": 2,
    "par_type": "thread",
    "default_tasks": ["binder"],
}


def task_release():
    """run all tasks, except re-locking"""
    return dict(
        file_dep=[
            *[P.OK / f"lint_{group}" for group in LINT_GROUPS],
            *P.SDISTS.values(),
            *P.WHEELS.values(),
            P.OK / "integrity",
            P.OK / "labextensions",
            P.OK / "nbtest",
            P.OK / "robot",
        ],
        actions=[lambda: print("OK to release")],
    )


def task_lock():
    """lock conda envs so they don't need to be solved in CI
    This should be run semi-frequently (e.g. after merge to master).
    Requires `conda-lock` CLI to be available
    """

    base_envs = [P.ENV.base, *P.ENV.WXYZ]
    test_envs = [*base_envs, P.ENV.utest, P.ENV.atest, P.ENV.lint]
    binder_args = None

    for task_args in iter_matrix(P.CI_TEST_MATRIX):
        if "linux-64" in task_args:
            binder_args = task_args
        matrix_envs = list(test_envs)
        if "win-64" in task_args:
            matrix_envs += [P.ENV.win]
        else:
            matrix_envs += [P.ENV.tpot, P.ENV.unix]

        yield make_lock_task("test", matrix_envs, P.CI_TEST_MATRIX, *task_args)

    for conda_platform in P.ALL_CONDA_PLATFORMS:
        yield make_lock_task("lock", [P.ENV.lock], {}, conda_platform, "3.8")

    yield make_lock_task(
        "binder", [*base_envs, P.ENV.tpot, P.ENV.binder], {}, *binder_args
    )


def task_setup_ts():
    """set up typescript environment"""
    return dict(
        file_dep=[*P.TS_PACKAGE, P.ROOT_PACKAGE],
        targets=[P.YARN_INTEGRITY, P.YARN_LOCK],
        actions=[["jlpm", "--prefer-offline"], ["jlpm", "lerna", "bootstrap"]],
    )


if P.RUNNING_IN_CI:

    def task_setup_py_ci():
        """CI: setup python packages from wheels"""
        return dict(
            file_dep=[*P.WHEELS.values()],
            targets=[P.OK / "setup_py"],
            actions=[
                U.okit("setup_py", remove=True),
                [
                    *P.PIP,
                    "install",
                    "--no-deps",
                    "--ignore-installed",
                    *P.WHEELS.values(),
                ],
                [*P.PIP, "freeze"],
                [*P.PIP, "check"],
                U.okit("setup_py"),
            ],
        )


else:

    def task_setup_py_dev():
        """ensure local packages are installed and editable"""

        def write_reqs_txt():
            """write out a requirements file so everything can be installed in one go"""
            P.BUILD.exists() or P.BUILD.mkdir()
            P.PY_DEV_REQS.write_text(
                "\n".join([f"-e {p.parent.relative_to(P.ROOT)}" for p in P.PY_SETUP])
            )

        yield dict(
            name="reqs_txt",
            targets=[P.PY_DEV_REQS],
            file_dep=[*P.ALL_SETUP_CFG, *P.PY_SETUP],
            actions=[write_reqs_txt],
        )

        yield dict(
            name="pip",
            file_dep=[P.PY_DEV_REQS],
            targets=[P.OK / "setup_py"],
            actions=[
                U.okit("setup_py", remove=True),
                [
                    *P.PIP,
                    "install",
                    "--no-deps",
                    "--ignore-installed",
                    "-r",
                    P.PY_DEV_REQS,
                ],
                [*P.PIP, "freeze"],
                [*P.PIP, "check"],
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

LINT_GROUPS["misc"] = [P.DODO, *P.SCRIPTS.glob("*.py"), *P.ATEST_PY]


def _make_linter(label, files):
    def _task():
        ok = f"lint_{label}"
        return dict(
            file_dep=[*files, P.OK / "setup_py"],
            actions=[
                U.okit(ok, remove=True),
                *[cmd + files for cmd in PY_LINT_CMDS if shutil.which(cmd[0])],
                U.okit(ok),
            ],
            targets=[P.OK / ok],
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
        pkg / "MANIFEST.in",
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
            actions=[
                lambda: [
                    shutil.rmtree(pkg / sub, ignore_errors=True)
                    for sub in ["build", f"{pkg.name}.egg-info"]
                ]
                and None,
                _action("sdist"),
                _action("bdist_wheel"),
            ],
            targets=[P.WHEELS[pkg.name], P.SDISTS[pkg.name]],
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
                [*P.PYM, "pytest", "-vv", "--no-coverage-upload"],
                cwd=P.PY_SRC / "wxyz_notebooks",
            )
            == 0,
            U.okit("nbtest"),
        ],
    )


if P.RUNNING_IN_BINDER:
    APP_DIR = ["--debug"]
else:
    APP_DIR = ["--debug", "--app-dir", P.LAB]


def task_lab_extensions():
    """set up local jupyterlab"""

    return dict(
        file_dep=[*P.TS_PACKAGE, *P.TS_TARBALLS, P.LABEXT_TXT],
        targets=[P.OK / "labextensions"],
        actions=[
            U.okit("labextensions", True),
            [
                *P.JPY,
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

    args = [*P.JPY, "lab", "build", "--dev-build=False", *APP_DIR]

    # binder runs out of memory
    if P.RUNNING_IN_BINDER:
        args += ["--minimize=False"]
    else:
        args += ["--minimize=True"]

    return dict(
        file_dep=[P.OK / "labextensions", *P.TS_TARBALLS],
        targets=[P.OK / "lab", P.LAB_INDEX],
        actions=[
            U.okit("lab", True),
            args,
            U.okit("lab"),
        ],
    )


def task_watch():
    """watch typescript sources, launch lab, rebuilding as files change"""

    def _watch():
        print(">>> Starting typescript watcher...", flush=True)
        ts = subprocess.Popen(["jlpm", "watch"])

        print(">>> Waiting a bit to start lab watcher...", flush=True)
        time.sleep(10)
        print(">>> Starting lab watcher...", flush=True)
        lab = subprocess.Popen(
            [*P.JPY, "lab", "--watch", "--no-browser", "--debug", *APP_DIR],
            stdin=subprocess.PIPE,
        )

        try:
            print(">>> Waiting for lab to exit (Ctrl+C)...", flush=True)
            lab.wait()
        except KeyboardInterrupt:
            print(
                ">>> Watch canceled by user!",
                flush=True,
            )
        finally:
            print(">>> Stopping watchers...", flush=True)
            ts.terminate()
            lab.terminate()
            lab.communicate(b"y\n")
            ts.wait()
            lab.wait()
            print(">>> Stopped watchers! maybe check process monitor...", flush=True)

        return True

    return dict(
        uptodate=[lambda: False],
        file_dep=[P.OK / "lab"],
        actions=[PythonInteractiveAction(_watch)],
    )


def task_update_binder():
    """pre-compute environment.yml for better caching on binder"""

    def make_binder_env():
        lock_lines = (
            P.BINDER_LOCKS[0].read_text().split("@EXPLICIT")[1].strip().splitlines()
        )
        P.BINDER_ENV.write_text(
            P.yaml.safe_dump(
                dict(
                    name="wxyz-binder",
                    channels=["conda-forge", "nodefaults"],
                    dependencies=lock_lines,
                ),
                default_flow_style=False,
            ),
        )

    return dict(
        file_dep=[*P.BINDER_LOCKS], targets=[P.BINDER_ENV], actions=[make_binder_env]
    )


def task_binder():
    """get to a working interactive state"""
    return dict(
        file_dep=[P.OK / "lab", P.OK / "setup_py"], actions=[lambda: print("OK")]
    )


ATEST = [P.PY, "-m", "_scripts._atest"]


def task_robot_lint():
    """format, then dry run robot syntax"""

    return dict(
        file_dep=[*P.ALL_ROBOT, *P.ALL_SRC_PY, *P.ALL_TS],
        targets=[P.OK / "robot_lint"],
        actions=[
            U.okit("robot_dry_run", remove=True),
            [*P.PYM, "robot.tidy", "--inplace", *P.ALL_ROBOT],
            [*ATEST, "--dryrun"],
            U.okit("robot_lint"),
        ],
    )


def task_robot():
    """test in browser with robot framework"""

    return dict(
        file_dep=sorted(
            [
                *P.ALL_ROBOT,
                *P.ALL_SRC_PY,
                *P.ATEST_PY,
                *P.ALL_TS,
                *P.ALL_IPYNB,
                P.LAB_INDEX,
                P.SCRIPTS / "_atest.py",
                P.OK / "lab",
                P.OK / "robot_lint",
            ]
        ),
        actions=[U.okit("robot", remove=True), [*ATEST], U.okit("robot")],
        targets=[P.OK / "robot"],
    )


def task_integrity():
    """check various sources of version and documentation issues"""
    return dict(
        file_dep=[*P.ALL_SRC_PY, *P.ALL_MD, *P.ALL_SETUP_CFG],
        actions=[
            U.okit("integrity", remove=True),
            [*P.PYM, "_scripts._integrity"],
            U.okit("integrity"),
        ],
        targets=[P.OK / "integrity"],
    )
