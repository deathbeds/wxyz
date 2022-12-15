""" environment locking for wxyz
"""
# pylint: disable=too-many-arguments,import-outside-toplevel,import-error

import collections
import itertools
import subprocess
import tempfile
from pathlib import Path

from doit.tools import config_changed

from . import _paths as P

# below here could move to a separate file

CHN = "channels"
DEP = "dependencies"


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
        with tempfile.TemporaryDirectory() as td:
            tdp = Path(td)
            rc = 1
            for extra_args in [[], ["--no-mamba"]]:
                args = [
                    "conda-lock",
                    "--mamba",
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
            tmp_lock_lines = tmp_lock_txt.splitlines()
            urls = [line for line in tmp_lock_lines if line.startswith("https://")]
            print(len(urls), "urls")
            if not lockfile.parent.exists():
                lockfile.parent.mkdir()
            lockfile.write_text(tmp_lock_txt)

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
