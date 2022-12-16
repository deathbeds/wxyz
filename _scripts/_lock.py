""" environment locking for wxyz
"""
# pylint: disable=too-many-arguments,import-outside-toplevel,import-error

import collections
import itertools
import subprocess
import tempfile
import textwrap
import typing
from pathlib import Path

from doit.tools import config_changed

from . import _paths as P

# below here could move to a separate file

CHN = "channels"
DEP = "dependencies"
EXPLICIT = "@EXPLICIT"


def _lock_comment(env_yamls: typing.List[Path]) -> str:
    deps = []
    for env_file in reversed(env_yamls):
        found_deps = False
        for line in env_file.read_text(encoding="utf-8").strip().splitlines():
            line = line.strip()
            if line.startswith("dependencies"):
                found_deps = True
            if not found_deps:
                continue
            if line.startswith("- "):
                deps += [line]
    comment = textwrap.indent("\n".join(sorted(set(deps))), "# ")
    return comment


def make_lock_task(kind_, env_files, config, platform_, python_, lab_=None):
    """generate a single dodo excursion for conda-lock"""
    lockfile = (
        P.LOCKS / f"conda.{kind_}.{platform_}-{python_}-{lab_ if lab_ else ''}.lock"
    )

    all_envs = [
        *env_files,
        P.REQS / f"py_{python_}.yml",
    ]

    if lab_:
        all_envs += [P.REQS / f"lab_{lab_}.yml"]

    file_dep = [*all_envs]

    def _lock():
        header = "\n".join([_lock_comment(all_envs), EXPLICIT]).strip()

        if lockfile.exists():
            lock_text = lockfile.read_text(encoding="utf-8")
            if lock_text.startswith(header):
                print(f"\t\t- {lockfile.name} is up-to-date (delete to force)")
                return True

        with tempfile.TemporaryDirectory() as td:
            tdp = Path(td)
            rc = 1
            for extra_args in [[], ["--no-mamba"]]:
                args = [
                    "conda-lock",
                    "--kind=explicit",
                    "--platform",
                    platform_,
                    *sum([["-f", str(p)] for p in all_envs], []),
                ] + extra_args
                print(">>>", " ".join(args), flush=True)
                rc = subprocess.call(args, cwd=str(tdp))
                if rc == 0:
                    break

            if rc != 0:
                raise Exception("couldn't solve at all", all_envs)

            tmp_lock = tdp / f"conda-{platform_}.lock"
            tmp_lock_txt = tmp_lock.read_text(encoding="utf-8")
            if not lockfile.parent.exists():
                lockfile.parent.mkdir()
            lockfile.write_text(
                "\n".join([header, tmp_lock_txt.split(EXPLICIT)[1].strip(), ""])
            )

        return True

    return dict(
        name=lockfile.name,
        uptodate=[config_changed(config)],
        file_dep=file_dep,
        actions=[_lock],
        targets=[lockfile],
    )


def expand_gh_matrix(matrix):
    """apply github matrix `include` and `exclude` transformations"""
    raw = dict(matrix)
    include = raw.pop("include", [])
    exclude = raw.pop("exclude", [])
    merged = [
        dict(collections.ChainMap(*p))
        for p in [*itertools.product(*[[{k: i} for i in raw[k]] for k in raw])]
    ]

    for m in merged:
        to_yield = dict(m)
        should_yield = True

        for inc in include or []:
            might_add = {}
            should_add = True
            for k, v in inc.items():
                mk = m.get(k)
                if mk is None:
                    might_add[k] = v
                elif mk != v:
                    should_add = False
            if should_add:
                to_yield.update(might_add)

        # if any of these match, skip yield
        for exc in exclude or []:
            should_yield = should_yield and not (
                all(m.get(k) == v for k, v in exc.items())
            )

        if should_yield:
            yield to_yield


def iter_matrix(matrix, keys=None):
    """generate a tuples of the keys for the github action matrix"""

    keys = keys or ["conda-subdir", "python-version", "lab"]

    for key in expand_gh_matrix(matrix):
        matrix_key = [key[k] for k in keys]
        yield tuple(matrix_key)


def lock_to_env(lock: Path, env: Path):
    """Generate a very explicit env from a lock."""
    env.write_text(
        P.RTD_ENV_TMPL.render(
            deps=lock.read_text(encoding="utf-8")
            .split(EXPLICIT)[1]
            .strip()
            .splitlines()
        )
    )
