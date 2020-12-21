""" wxyz top-level automation

    this should be executed from within an environment created from
    the ci/locks/conda.*.lock appropriate for your platform. See CONTRIBUTING.md.
"""
# pylint: disable=expression-not-assigned,W0511

import json
import shutil
import subprocess
import time
from configparser import ConfigParser
from hashlib import sha256

from doit.tools import PythonInteractiveAction, config_changed

from _scripts import _paths as P
from _scripts import _util as U
from _scripts._lock import iter_matrix, make_lock_task

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
            *[P.OK / f"lint_{group}" for group in P.LINT_GROUPS],
            P.SHA256SUMS,
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
            matrix_envs += [P.ENV.tpot, P.ENV.win, P.ENV.win_tpot]
        else:
            matrix_envs += [P.ENV.tpot, P.ENV.unix, P.ENV.unix_tpot]

        yield make_lock_task("test", matrix_envs, P.CI_TEST_MATRIX, *task_args)

    for conda_platform in P.ALL_CONDA_PLATFORMS:
        yield make_lock_task("lock", [P.ENV.lock], {}, conda_platform, "3.8")

    yield make_lock_task(
        "binder",
        [*base_envs, P.ENV.tpot, P.ENV.unix_tpot, P.ENV.binder],
        {},
        *binder_args,
    )

    yield make_lock_task(
        "docs",
        [*test_envs, P.ENV.lint, P.ENV.docs],
        {},
        *binder_args,
    )


def task_setup_ts():
    """set up typescript environment"""
    return dict(
        file_dep=[*P.TS_PACKAGE, P.ROOT_PACKAGE],
        targets=[P.YARN_INTEGRITY, P.YARN_LOCK],
        actions=[
            ["jlpm", "--prefer-offline", "--ignore-optional"],
            ["jlpm", "lerna", "bootstrap"],
        ],
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


if not P.TESTING_IN_CI:

    def task_lint_prettier():
        """use prettier to format things"""

        yield dict(
            name="core",
            uptodate=[config_changed(P.README.read_text())],
            file_dep=[P.YARN_INTEGRITY, P.YARN_LOCK],
            actions=[["jlpm", "prettier", "--write", "--list-different", P.README]],
            targets=[P.README],
        )

        yield dict(
            name="rest",
            file_dep=[P.YARN_INTEGRITY, P.YARN_LOCK, *P.ALL_PRETTIER],
            targets=[P.OK / "prettier"],
            actions=[
                U.okit("prettier", remove=True),
                ["jlpm", "lint"],
                U.okit("prettier"),
            ],
        )


def _make_linter(label, files):
    def _task():
        # pylint: disable=not-callable
        ok = f"lint_{label}"
        return dict(
            file_dep=[*files, P.OK / "setup_py"],
            actions=[
                U.okit(ok, remove=True),
                *sum(
                    [
                        cmd[0](files) if callable(cmd[0]) else [cmd + files]
                        for cmd in P.PY_LINT_CMDS
                        if callable(cmd[0]) or shutil.which(cmd[0])
                    ],
                    [],
                ),
                U.okit(ok),
            ],
            targets=[P.OK / ok],
        )

    _task.__name__ = f"task_lint_py_{label}"
    _task.__doc__ = f"format/lint {label}"

    return {_task.__name__: _task}


if not P.TESTING_IN_CI:
    [
        globals().update(_make_linter(label, files))
        for label, files in P.LINT_GROUPS.items()
    ]


def _make_schema(source, targets):
    schema = P.SCHEMA / f"{source.stem}.schema.json"

    yield dict(
        name=schema.name,
        file_dep=[source, P.YARN_INTEGRITY],
        actions=[
            lambda: [P.SCHEMA.mkdir(parents=True, exist_ok=True), None][-1],
            [
                P.JLPM,
                "--silent",
                "ts-json-schema-generator",
                "--path",
                source,
                "--out",
                schema,
            ],
        ],
        targets=[schema],
    )
    for target in targets:
        yield dict(
            name=target.name,
            file_dep=[schema, P.SCRIPTS / "_ts2w.py", P.YARN_INTEGRITY],
            actions=[[*P.PYM, "_scripts._ts2w", schema, target]],
            targets=[target],
        )


def task_schema():
    """update code files from schema"""
    for source, targets in P.SCHEMA_WIDGETS.items():
        for task in _make_schema(source, targets):
            yield task


def _make_pydist(setup_py):
    """build python release artifacts"""
    pkg = setup_py.parent
    file_dep = [
        setup_py,
        pkg / "setup.cfg",
        pkg / "MANIFEST.in",
        pkg / "LICENSE.txt",
        pkg / "README.md",
        *sorted((pkg / "src").rglob("*.py")),
    ]

    def _action(output):
        """build a single task so we can run in the cwd"""
        args = [P.PY, "setup.py", output, "--dist-dir", P.DIST]
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


def task_hash_dist():
    """make a hash bundle of the dist artifacts"""

    def _run_hash():
        # mimic sha256sum CLI
        if P.SHA256SUMS.exists():
            P.SHA256SUMS.unlink()

        lines = []

        for p in P.HASH_DEPS:
            if p.parent != P.DIST:
                tgt = P.DIST / p.name
                if tgt.exists():
                    tgt.unlink()
                shutil.copy2(p, tgt)
            lines += ["  ".join([sha256(p.read_bytes()).hexdigest(), p.name])]

        output = "\n".join(lines)
        print(output)
        P.SHA256SUMS.write_text(output)

    return dict(actions=[_run_hash], file_dep=P.HASH_DEPS, targets=[P.SHA256SUMS])


def task_ts():
    """build typescript components"""

    file_dep = [
        P.YARN_LOCK,
        *P.TS_PACKAGE,
        *P.TS_READMES,
        *P.TS_LICENSES,
    ]

    if not P.TESTING_IN_CI:
        file_dep += [P.OK / "prettier"]

    return dict(
        file_dep=file_dep,
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
                [*P.PYM, "pytest", "-vv", "-n", "auto", "--no-coverage-upload"],
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


def _make_py_readme(setup_py):
    pkg = setup_py.parent
    setup_cfg = pkg / "setup.cfg"

    readme = pkg / "README.md"
    license_ = pkg / "LICENSE.txt"

    def _write():
        license_.write_text(P.LICENSE.read_text())
        parser = ConfigParser()
        parser.read(setup_cfg)
        context = {s: dict(parser[s]) for s in parser.sections()}

        for package_json in P.TS_PACKAGE_CONTENT.values():
            lab = package_json.get("jupyterlab")
            if lab is None:
                continue
            if pkg.name == lab["discovery"]["server"]["base"]["name"]:
                context["js_pkg"] = package_json
                break

        readme.write_text(
            "\n\n".join(
                [P.PY_README_TMPL.render(**context), "---", P.README.read_text()]
            ).strip()
        )

    return dict(
        name=pkg.name,
        uptodate=[config_changed(P.PY_README_TXT)],
        actions=[
            _write,
            ["jlpm", "prettier", "--write", "--list-different", readme],
        ],
        file_dep=[P.README, setup_cfg],
        targets=[readme, license_],
    )


def _make_ts_readme(package_json):
    pkg = package_json.parent

    readme = pkg / "README.md"
    license_ = pkg / "LICENSE.txt"

    def _write():
        license_.write_text(P.LICENSE.read_text())
        context = json.loads(package_json.read_text(encoding="utf-8"))
        readme.write_text(
            "\n\n".join(
                [P.TS_README_TMPL.render(**context), "---", P.README.read_text()]
            ).strip()
        )

    return dict(
        name=pkg.name,
        uptodate=[config_changed(P.TS_README_TXT)],
        actions=[
            _write,
            ["jlpm", "prettier", "--write", "--list-different", readme],
        ],
        file_dep=[P.README, package_json],
        targets=[readme, license_],
    )


if not P.TESTING_IN_CI:

    def task_docs():
        """make the docs right"""

        for setup_py in P.PY_SETUP:
            yield _make_py_readme(setup_py)

        for package_json in P.TS_PACKAGE:
            if package_json.parent.name == "wxyz-meta":
                continue
            yield _make_ts_readme(package_json)

        if shutil.which("sphinx-build"):
            yield dict(
                name="sphinx",
                doc="build the HTML site",
                actions=[["sphinx-build", "-b", "dirhtml", "docs", "build/docs"]],
                file_dep=[
                    P.DOCS_CONF_PY,
                    *P.ALL_SRC_PY,
                    *P.ALL_SETUP_CFG,
                    P.OK / "setup_py"
                ],
                targets=[P.DOCS_BUILDINFO],
            )


def _make_spell(path):
    rel = path.relative_to(P.DOCS_OUT)
    spell_key = "spell_" + str(rel.as_posix()).replace("/", "_").replace(".", "/")
    args = ["hunspell", "-d", P.SPELL_LANGS, "-p", P.DICTIONARY, "-l", "-H", path]

    def _spell():
        misspelled = [
            line.strip()
            for line in subprocess.check_output(args).decode("utf-8").splitlines()
            if line.strip()
        ]

        if misspelled:
            print(">> misspelled words in ", path)
            print("\n".join(sorted(set(misspelled))))
            return False

        return True

    return dict(
        name=spell_key,
        file_dep=[path, P.DICTIONARY, P.README],
        actions=[U.okit(spell_key, remove=True), _spell, U.okit(spell_key)],
        targets=[P.OK / spell_key],
    )


if shutil.which("hunspell"):

    def task_spell():
        """check spelling of built HTML site"""
        if shutil.which("hunspell"):
            for path in P.ALL_SPELL_DOCS:
                yield _make_spell(path)


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


def task_binder():
    """get to a working interactive state"""
    return dict(
        file_dep=[P.OK / "lab", P.OK / "setup_py"], actions=[lambda: print("OK")]
    )


ATEST = [P.PY, "-m", "_scripts._atest"]


def task_robot_lint():
    """format, then dry run robot syntax"""

    return dict(
        file_dep=[*P.ALL_ROBOT, *P.ATEST_PY],
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
        file_dep=[
            *P.ALL_SRC_PY,
            *P.ALL_MD,
            *P.ALL_SETUP_CFG,
            P.POSTBUILD,
            P.SCRIPTS / "_integrity.py",
        ],
        actions=[
            U.okit("integrity", remove=True),
            [*P.PYM, "_scripts._integrity"],
            U.okit("integrity"),
        ],
        targets=[P.OK / "integrity"],
    )
