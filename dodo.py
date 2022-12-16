""" wxyz top-level automation

    this should be executed from within an environment created from
    the .github/locks/conda.*.lock appropriate for your platform. See CONTRIBUTING.md.
"""
import json
import os

# pylint: disable=expression-not-assigned,W0511,too-many-lines
import shutil
import subprocess
import time
from hashlib import sha256

try:
    import ipywidgets
except ImportError:
    pass

from doit import create_after
from doit.tools import PythonInteractiveAction, config_changed

from _scripts import _paths as P
from _scripts import _util as U
from _scripts._lock import iter_matrix, make_lock_task

DOIT_CONFIG = {
    "backend": "sqlite3",
    "verbosity": 2,
    "par_type": "thread",
    "default_tasks": ["binder"],
    "reporter": U.Reporter,
}

os.environ.update(PIP_NO_BUILD_ISOLATION="1")


def task_release():
    """run all tasks, except re-locking and docs"""
    return dict(
        file_dep=[
            *sum(
                [
                    [P.OK / f"lint_{group}_1_pylint", P.OK / f"lint_{group}_1_flake8"]
                    for group in P.LINT_GROUPS
                ],
                [],
            ),
            P.SHA256SUMS,
            P.OK / "integrity",
            P.OK / "nbtest",
            P.OK / "robot",
        ],
        targets=[P.OK / "release"],
        actions=[
            U.okit("release", remove=True),
            lambda: print("OK to release"),
            U.okit("release"),
        ],
    )


if not P.RUNNING_IN_CI:

    @create_after("docs")
    def task_all():
        """like release, but also builds docs (no locks)"""
        return dict(
            file_dep=[P.SHA256SUMS, P.OK / "release"],
            task_dep=["spell", "checklinks"],
            actions=[lambda: print("OK to docs")],
        )


if not (P.TESTING_IN_CI or P.BUILDING_IN_CI):

    def task_lock():
        """lock conda envs so they don't need to be solved in CI
        This should be run semi-frequently (e.g. after merge to `main`).
        Requires `conda-lock` CLI to be available

        TODO: this should be more deriveable directly from a file tree structure
              that matches a github actions schema
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
                matrix_envs += [P.ENV.unix]

            yield make_lock_task("test", matrix_envs, P.CI_TEST_MATRIX, *task_args)

        for conda_platform in P.ALL_CONDA_PLATFORMS:
            yield make_lock_task("lock", [P.ENV.lock], {}, conda_platform, "3.8")

        yield make_lock_task(
            "binder",
            [*base_envs, P.ENV.binder],
            {},
            *binder_args,
        )

        yield make_lock_task(
            "docs",
            [*test_envs, P.ENV.lint, P.ENV.docs],
            {},
            *binder_args,
        )


if not P.TESTING_IN_CI:

    def task_setup_ts():
        """set up typescript environment"""
        dep_types = ["devDependencies", "dependencies", "peerDependencies"]
        return dict(
            uptodate=[
                config_changed(
                    {
                        pkg["name"]: {dep: pkg.get(dep) for dep in dep_types}
                        for pkg in P.TS_PACKAGE_CONTENT.values()
                    }
                )
            ],
            file_dep=[P.ROOT_PACKAGE],
            targets=[P.YARN_INTEGRITY, P.YARN_LOCK],
            actions=[
                [
                    "jlpm",
                    "--prefer-offline",
                    "--ignore-optional",
                    "--ignore-scripts",
                    "--registry=https://registry.npmjs.org",
                ],
                ["jlpm", "yarn-deduplicate", "--strategy", "fewer", "--fail"],
                ["jlpm", "lerna", "bootstrap"],
            ],
        )


if P.RUNNING_IN_CI:

    def task_setup_py_ci():
        """CI: setup python packages from wheels"""
        return dict(
            file_dep=[*P.WHEELS.values()],
            targets=[P.OK / "setup_py", P.OK / "setup_lab"],
            actions=[
                U.okit("setup_py", remove=True),
                U.okit("setup_lab", remove=True),
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
                ["jupyter", "labextension", "list"],
                U.okit("setup_lab"),
            ],
        )

else:

    def task_setup_py_dev():
        """ensure local packages are installed and editable"""

        def write_reqs_txt():
            """write out a requirements file so everything can be installed in one go"""
            P.BUILD.exists() or P.BUILD.mkdir()
            P.PY_DEV_REQS.write_text(
                "\n".join(
                    [f"-e {p.parent.relative_to(P.ROOT)}" for p in P.ALL_PYPROJECT_TOML]
                )
            )

        yield dict(
            name="reqs_txt",
            targets=[P.PY_DEV_REQS],
            file_dep=[*P.ALL_PYPROJECT_TOML],
            actions=[write_reqs_txt],
        )

        yield dict(
            name="pip",
            file_dep=[P.PY_DEV_REQS, *P.TS_D_PACKAGE_JSON.values()],
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

        yield dict(
            name="lab",
            file_dep=[P.PY_DEV_REQS, P.OK / "setup_py"],
            targets=[P.OK / "setup_lab"],
            actions=[
                U.okit("setup_lab", remove=True),
                *[(_make_develop, [p.parent]) for p in P.WXYZ_LAB_EXTENSIONS],
                ["jupyter", "labextension", "list"],
                U.okit("setup_lab"),
            ],
        )


def _make_develop(path):
    args = [
        *P.PYM,
        "_scripts._hacked_labextension",
        "develop",
        "--debug",
        "--overwrite",
        f"wxyz.{path.name}",
    ]
    # py_path = path.parent.parent.parent
    # raise Exception(args)
    return subprocess.call(args) == 0


def _make_linters(label, files):
    prev = [P.OK / "setup_py"]
    next_prev = []

    for i, cmd_group in enumerate(P.PY_LINT_CMDS):
        for linter, cmd in cmd_group.items():
            ok = f"lint_{label}_{i}_{linter}"
            next_prev += [P.OK / ok]

            yield dict(
                name=f"{label}:{linter}",
                file_dep=[*files, *prev] if prev else [*files, P.OK / "setup_py"],
                actions=[
                    U.okit(ok, remove=True),
                    *(cmd(files) if callable(cmd) else [cmd + files]),
                    U.okit(ok),
                ],
                targets=[P.OK / ok],
            )
        prev = next_prev
        next_prev = []


if not (P.TESTING_IN_CI or P.BUILDING_IN_CI):

    def task_lint():
        """detect and (hopefully) correct code style/formatting"""
        for label, files in P.LINT_GROUPS.items():
            for linter in _make_linters(label, files):
                yield linter

        yield dict(
            name="prettier:core",
            uptodate=[config_changed(P.README.read_text(encoding="utf-8"))],
            file_dep=[P.YARN_INTEGRITY, P.YARN_LOCK],
            actions=[["jlpm", "prettier", "--write", "--list-different", P.README]],
            targets=[P.README],
        )

        yield dict(
            name="prettier:rest",
            file_dep=[P.YARN_INTEGRITY, P.YARN_LOCK, *P.ALL_PRETTIER],
            targets=[P.OK / "prettier"],
            actions=[
                U.okit("prettier", remove=True),
                ["jlpm", "lint:prettier"],
                U.okit("prettier"),
            ],
        )

        yield dict(
            name="robot",
            file_dep=[*P.ALL_ROBOT, *P.ATEST_PY],
            targets=[P.OK / "robot_lint"],
            actions=[
                U.okit("robot_dry_run", remove=True),
                [*P.PYM, "robotidy", *P.ALL_ROBOT],
                [*ATEST, "--dryrun"],
                U.okit("robot_lint"),
            ],
        )


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


if not P.RUNNING_IN_CI:

    def task_schema():
        """update code files from schema"""
        for source, targets in P.SCHEMA_WIDGETS.items():
            for task in _make_schema(source, targets):
                yield task


def _make_pydist(pyproj):
    """build python release artifacts"""
    pkg = pyproj.parent
    file_dep = [pyproj, pkg / P.LICENSE_NAME, *sorted((pkg / "src").rglob("*.py"))]

    if pkg in P.TS_D_PACKAGE_JSON:
        file_dep += [P.TS_D_PACKAGE_JSON[pkg]]

    wheel, sdist = P.WHEELS[pkg.name], P.SDISTS[pkg.name]

    yield dict(
        name=pkg.name,
        doc=f"build {pkg.name} distributions",
        file_dep=file_dep,
        actions=[
            (U.call, [["flit", "build"]], {"cwd": pkg}),
            (U.copy_one, [pkg / f"dist/{sdist.name}", sdist]),
            (U.copy_one, [pkg / f"dist/{wheel.name}", wheel]),
        ],
        targets=[wheel, sdist],
    )


def task_dist():
    """make pypi distributions"""
    if P.TESTING_IN_CI:
        return

    for ppt in P.ALL_PYPROJECT_TOML:
        yield _make_pydist(ppt)


def task_hash_dist():
    """make a hash bundle of the dist artifacts"""
    if P.TESTING_IN_CI:
        return

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


def _make_lab_ext_build(ext):
    tsp_json = P.TS_PACKAGE_CONTENT[ext / "package.json"]
    target = (ext / tsp_json["jupyterlab"]["outputDir"] / "package.json").resolve()

    yield dict(
        name=f"""ext:{ext.name}""".replace("/", "_"),
        file_dep=[
            ext / "lib" / ".tsbuildinfo",
            ext / "README.md",
            ext / "LICENSE.txt",
            *ext.rglob("style/*.css"),
            ext / "package.json",
        ],
        actions=[
            lambda: subprocess.call([*P.LAB_EXT, "build", "."], cwd=str(ext)) == 0
        ],
        targets=[target],
    )


if not P.TESTING_IN_CI:

    def task_ts():
        """build typescript components"""

        file_dep = [P.YARN_LOCK, *P.TS_PACKAGE, *P.ALL_TS]

        if not P.BUILDING_IN_CI:
            file_dep += [P.OK / "prettier"]

        yield dict(
            name="tsc",
            file_dep=file_dep,
            targets=P.TS_ALL_BUILD,
            actions=[["jlpm", "build:ts"]],
        )

        yield dict(
            name="pack",
            file_dep=[
                P.TS_META_BUILD,
                *P.TS_READMES,
                *P.TS_LICENSES,
            ],
            actions=[["jlpm", "build:tgz"]],
            targets=[*P.TS_TARBALLS],
        )

        for ext in P.WXYZ_LAB_EXTENSIONS:
            for task in _make_lab_ext_build(ext):
                yield task


if not P.BUILDING_IN_CI:

    def task_nbtest():
        """smoke test all notebooks with nbconvert"""

        env = dict(os.environ)
        env.update(WXYZ_WIDGET_LOG_OUT=str(P.WIDGET_LOG_OUT))

        return dict(
            file_dep=[*P.ALL_SRC_PY, *P.ALL_IPYNB, P.OK / "setup_py"],
            targets=[P.OK / "nbtest"],
            actions=[
                lambda: [P.WIDGET_LOG_OUT.exists() or P.WIDGET_LOG_OUT.mkdir(), None][
                    -1
                ],
                U.okit("nbtest", True),
                lambda: U.call(
                    [
                        *P.PYM,
                        "pytest",
                        "-vv",
                        "-n",
                        "auto",
                        "-o",
                        f"junit_suite_name=nbtest_{P.OS}_{P.PY_VER}",
                        *os.environ.get("WXYZ_PYTEST_ARGS", "").split("  "),
                    ],
                    cwd=P.PY_SRC / "wxyz_notebooks",
                    env=env,
                )
                == 0,
                U.okit("nbtest"),
            ],
        )


def _make_py_readme(py_proj):
    pkg = py_proj.parent

    readme = pkg / "README.md"

    def _write():
        context = {**P.PY_PROJ[py_proj]}

        for package_json in P.TS_PACKAGE_CONTENT.values():
            lab = package_json.get("jupyterlab")
            if lab is None:
                continue
            if pkg.name == lab["discovery"]["server"]["base"]["name"]:
                context["js_pkg"] = package_json
                break

        readme.write_text(
            "\n\n".join(
                [
                    P.PY_README_TMPL.render(**context),
                    "---",
                    P.README.read_text(encoding="utf-8"),
                ]
            ).strip()
        )

    return dict(
        name=f"readme:py:{pkg.name}",
        uptodate=[config_changed(P.PY_README_TXT)],
        actions=[
            _write,
            ["jlpm", "--silent", "prettier", "--write", "--list-different", readme],
        ],
        file_dep=[P.README, py_proj],
        targets=[readme],
    )


def _make_ts_readme(package_json):
    pkg = package_json.parent
    readme = pkg / "README.md"
    license_ = pkg / P.LICENSE_NAME

    def _write():
        license_.write_text(P.LICENSE.read_text(encoding="utf-8"))
        context = json.loads(package_json.read_text(encoding="utf-8"))
        readme.write_text(
            "\n\n".join(
                [
                    P.TS_README_TMPL.render(**context),
                    "---",
                    P.README.read_text(encoding="utf-8"),
                ]
            ).strip()
        )

    return dict(
        name=f"readme:ts:{pkg.name}",
        uptodate=[config_changed(P.TS_README_TXT)],
        actions=[
            _write,
            ["jlpm", "prettier", "--write", "--list-different", readme],
        ],
        file_dep=[P.README, package_json],
        targets=[readme, license_],
    )


def _make_py_rst(setup_py):
    pkg = setup_py.parent.name
    name = pkg.replace("wxyz_", "")
    out = P.DOCS / "widgets"
    target = out / f"""{name}.rst"""
    module = pkg.replace("_", ".", 1)

    def _write():
        if not out.exists():
            out.mkdir()
        target.write_text(
            P.PY_RST_TEMPLATE.render(
                name=name,
                module=module,
                stars="*" * len(module),
                exclude_members=", ".join(dir(ipywidgets.DOMWidget)),
            )
        )

    return dict(
        name=f"rst:{setup_py.parent.name}",
        actions=[_write],
        targets=[target],
        uptodate=[config_changed(P.PY_RST_TEMPLATE_TXT)],
        file_dep=[*(setup_py.parent / "src").rglob("*.py"), P.OK / "setup_py"],
    )


def _make_widget_index(file_dep):
    target = P.DOCS / "widgets.ipynb"

    def _write():
        nb_json = json.loads(target.read_text(encoding="utf-8"))
        toc = None
        for cell in nb_json["cells"]:
            if cell["cell_type"] == "markdown":
                for line in cell["source"]:
                    if "<!-- BEGIN MODULEGEN" in line:
                        toc = cell

        toc["source"] = [
            "<!-- BEGIN MODULEGEN -->\n",
            """```{toctree}\n""",
            """:maxdepth: 3\n""",
            *[
                f"""widgets/{d.stem.replace("wxyz_", "")}""" + "\n"
                for d in file_dep
                if d.suffix == ".rst"
            ],
            "```\n",
            "<!-- END MODULEGEN -->\n",
        ]
        target.write_text(json.dumps(nb_json, indent=2), encoding="utf-8")

    return dict(
        name="ipynb:modindex", actions=[_write], targets=[target], file_dep=file_dep
    )


def _make_dot(setup_py):
    pkg = setup_py.parent.name
    name = pkg.replace("wxyz_", "")
    out = P.DOCS / "widgets" / "dot"
    module = pkg.replace("_", ".", 1)
    target = out / f"classes_{name}.dot"
    py_files = [*setup_py.parent.rglob("*.py")]

    def _make():
        if not out.exists():
            out.mkdir()

        modules = [module]
        if "notebooks" not in name:
            modules += [f"{module}.base"]

        with subprocess.Popen(
            [*P.PYREVERSE, "-p", name, *modules],
            cwd=out,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ) as proc:
            pstdout, pstderr = proc.communicate()

            if proc.returncode != 0:
                raise RuntimeError(
                    "\n".join(
                        [
                            "stdout:\n",
                            pstdout.decode("utf-8"),
                            "\nstderr:\n",
                            pstderr.decode("utf-8"),
                            "-----",
                            f"ERROR {proc.returncode}",
                        ]
                    )
                )

        ugly_packages = out / f"packages_{name}.dot"
        if ugly_packages.exists():
            ugly_packages.unlink()
        dot_txt = target.read_text(encoding="utf-8")

        for py_file in py_files:
            replace_name = f"wxyz.{name}"
            if py_file.stem == "base":
                replace_name += ".base"
            dot_txt = dot_txt.replace(str(py_file), replace_name)

        dot_lines = dot_txt.splitlines()

        target.write_text(
            "\n".join(
                [
                    dot_lines[0],
                    """
            graph [fontname = "sans-serif"];
            node [fontname = "sans-serif"];
            edge [fontname = "sans-serif"];
            """,
                    *dot_lines[1:],
                ]
            )
        )

    return dict(
        name=f"dot:{name}",
        actions=[_make],
        uptodate=[config_changed({"args": P.PYREVERSE})],
        file_dep=[*py_files, P.OK / "setup_py"],
        targets=[target],
    )


if not (P.TESTING_IN_CI or P.BUILDING_IN_CI):

    def task_docs():
        """make the docs right"""
        widget_index_deps = []

        for py_proj in P.PY_PROJ:
            yield _make_py_readme(py_proj)

            task = _make_py_rst(py_proj)
            yield task
            widget_index_deps += task["targets"]

        yield _make_widget_index(widget_index_deps)

        for package_json in P.TS_PACKAGE:
            if "meta" not in package_json.parent.name:
                yield _make_ts_readme(package_json)

        yield dict(
            name="favicon",
            actions=[[*P.PYM, "_scripts._favicon"]],
            file_dep=[P.DOCS_LOGO],
            targets=[P.DOCS_FAVICON],
        )

        if shutil.which("sphinx-build"):
            yield dict(
                name="sphinx",
                doc="build the HTML site",
                actions=[["sphinx-build", "-j8", "-b", "html", "docs", "build/docs"]],
                file_dep=[
                    *P.ALL_PYPROJECT_TOML,
                    *P.ALL_SRC_PY,
                    *P.DOCS_DOT,
                    *P.DOCS_IPYNB,
                    *P.DOCS_STATIC.rglob("*"),
                    *P.DOCS_TEMPLATES,
                    *P.PY_DOCS_RST,
                    P.DOCS_CONF_PY,
                    P.OK / "setup_py",
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


if not (P.TESTING_IN_CI or P.BUILDING_IN_CI) and shutil.which("hunspell"):

    @create_after("docs")
    def task_spell():
        """check spelling of built HTML site"""
        if shutil.which("hunspell"):
            for path in P.ALL_SPELL_DOCS():
                yield _make_spell(path)


if not (P.TESTING_IN_CI or P.BUILDING_IN_CI) and shutil.which("pytest-check-links"):

    @create_after("docs")
    def task_checklinks():
        """check whether links in built docs are valid"""
        key = "check_links"
        args = [
            "pytest-check-links",
            "-o",
            "junit_suite_name=checklinks",
            "--check-anchors",
            "--check-links-cache",
            "--check-links-cache-name=build/check_links/cache",
            # a few days seems reasonable
            f"--check-links-cache-expire-after={60 * 60 * 24 * 3}",
            # might be able to relax this, eventually
            "-k",
            "not (master or carousel)",
        ]
        return dict(
            uptodate=[config_changed(dict(args=args))],
            actions=[
                U.okit(key, remove=True),
                lambda: (P.BUILD / "check_links/cache").mkdir(
                    parents=True, exist_ok=True
                ),
                [
                    *args,
                    P.DOCS_OUT,
                ],
                U.okit(key),
            ],
            file_dep=[*P.ALL_SPELL_DOCS()],
            targets=[P.OK / key],
        )


if not P.RUNNING_IN_CI:

    def _make_lab(watch=False):
        # pylint: disable=consider-using-with
        def _lab():
            if watch:
                print(">>> Starting typescript watcher...", flush=True)
                ts = subprocess.Popen(["jlpm", "watch"])

                ext_watchers = [
                    subprocess.Popen([*P.LAB_EXT, "watch", "."], cwd=str(p))
                    for p in P.WXYZ_LAB_EXTENSIONS
                ]

                print(">>> Waiting a bit to JupyterLab...", flush=True)
                time.sleep(3)
            print(">>> Starting JupyterLab...", flush=True)
            lab = subprocess.Popen(
                [*P.JPY, "lab", "--no-browser", "--debug"],
                stdin=subprocess.PIPE,
            )

            try:
                print(">>> Waiting for JupyterLab to exit (Ctrl+C)...", flush=True)
                lab.wait()
            except KeyboardInterrupt:
                print(
                    f""">>> {"Watch" if watch else "Run"} canceled by user!""",
                    flush=True,
                )
            finally:
                print(">>> Stopping watchers...", flush=True)
                if watch:
                    [x.terminate() for x in ext_watchers]
                    ts.terminate()
                lab.terminate()
                lab.communicate(b"y\n")
                if watch:
                    ts.wait()
                    lab.wait()
                    [x.wait() for x in ext_watchers]
                    print(
                        ">>> Stopped watchers! maybe check process monitor...",
                        flush=True,
                    )

            return True

        return _lab

    def task_lab():
        """start JupyterLab, no funny stuff (Note: Single Ctrl+C stops)"""
        yield dict(
            name="serve",
            uptodate=[lambda: False],
            file_dep=[P.OK / "setup_lab"],
            actions=[PythonInteractiveAction(_make_lab())],
        )

    def task_watch():
        """watch typescript sources, launch JupyterLab, rebuilding as files change"""

        yield dict(
            name="lab",
            uptodate=[lambda: False],
            file_dep=[P.OK / "setup_lab"],
            actions=[PythonInteractiveAction(_make_lab(watch=True))],
        )

        def _docs():
            p = None
            args = [
                "sphinx-autobuild",
                "-a",
                "-j8",
                "--re-ignore",
                r"'*\.ipynb_checkpoints*'",
                P.DOCS,
                P.DOCS_OUT,
            ]
            with subprocess.Popen(args) as p:
                try:
                    p.wait()
                finally:
                    p.terminate()
                    p.wait()

        if shutil.which("sphinx-autobuild"):
            yield dict(
                name="docs",
                doc="serve docs, watch (some) sources, livereload (when it can)",
                uptodate=[lambda: False],
                file_dep=[P.DOCS_BUILDINFO],
                actions=[PythonInteractiveAction(_docs)],
            )


if not (P.TESTING_IN_CI or P.BUILDING_IN_CI):

    def task_binder():
        """get to a working interactive state"""
        return dict(
            file_dep=[P.OK / "setup_lab", P.OK / "setup_py"],
            actions=[lambda: print("OK")],
        )


ATEST = [P.PY, "-m", "_scripts._atest"]


if not P.BUILDING_IN_CI:

    def task_robot():
        """test in browser with robot framework"""

        file_dep = [
            *P.ALL_ROBOT,
            *P.ALL_SRC_PY,
            *P.ATEST_PY,
            *P.ALL_TS,
            *P.ALL_IPYNB,
            P.SCRIPTS / "_atest.py",
            P.OK / "setup_lab",
        ]

        if not P.RUNNING_IN_CI:
            file_dep += [P.OK / "robot_lint"]

        return dict(
            file_dep=sorted(file_dep),
            actions=[U.okit("robot", remove=True), [*ATEST], U.okit("robot")],
            targets=[P.OK / "robot"],
        )


if not (P.BUILDING_IN_CI or P.TESTING_IN_CI):

    def task_integrity():
        """check various sources of version and documentation issues"""
        return dict(
            file_dep=[
                *P.ALL_SRC_PY,
                *P.ALL_MD,
                *P.ALL_PYPROJECT_TOML,
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
