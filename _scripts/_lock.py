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

try:
    from ruamel_yaml import safe_dump, safe_load
except ImportError:
    from yaml import safe_dump, safe_load


# below here could move to a separate file

CHN = "channels"
DEP = "dependencies"


def make_lock_task(kind_, env_files, config, platform_, python_, lab_=None):
    """generate a single dodo excursion for conda-lock"""
    lockfile = (
        P.LOCKS / f"conda.{kind_}.{platform_}-{python_}-{lab_ if lab_ else ''}.lock"
    )
    file_dep = [*env_files]

    def expand_specs(specs):
        from conda.models.match_spec import MatchSpec

        for raw in specs:
            match = MatchSpec(raw)
            yield match.name, [raw, match]

    def merge(composite, env):
        if CHN in env and env[CHN]:
            composite[CHN] = env[CHN]

        comp_specs = dict(expand_specs(composite.get(DEP, [])))
        env_specs = dict(expand_specs(env.get(DEP, [])))

        deps = [raw for (raw, match) in env_specs.values()]
        deps += [
            raw for name, (raw, match) in comp_specs.items() if name not in env_specs
        ]

        composite[DEP] = sorted(deps)

        return composite

    def _lock():
        composite = dict()

        for env_dep in env_files:
            print(f"merging {env_dep.name}", flush=True)
            composite = merge(composite, safe_load(env_dep.read_text(encoding="utf-8")))

        fake_deps = []

        if python_:
            fake_deps += [f"python ={python_}.*"]
        if lab_:
            fake_deps += [f"jupyterlab ={lab_}.*"]

        fake_env = {DEP: fake_deps}

        composite = merge(composite, fake_env)

        with tempfile.TemporaryDirectory() as td:
            tdp = Path(td)
            composite_yml = tdp / "composite.yml"
            composite_yml.write_text(safe_dump(composite, default_flow_style=False))
            print(
                "composite\n\n",
                composite_yml.read_text(encoding="utf-8"),
                "\n\n",
                flush=True,
            )
            rc = 1
            for extra_args in [[], ["--no-mamba"]]:
                args = [
                    "conda-lock",
                    "-p",
                    platform_,
                    "-f",
                    str(composite_yml),
                ] + extra_args
                print(">>>", " ".join(args), flush=True)
                rc = subprocess.call(args, cwd=str(tdp))
                if rc == 0:
                    break

            if rc != 0:
                raise Exception("couldn't solve at all", composite)

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
                all([m.get(k) == v for k, v in exc.items()])
            )

        if should_yield:
            yield to_yield


def iter_matrix(matrix, keys=None):
    """generate a tuples of the keys for the github action matrix"""

    keys = keys or ["conda-subdir", "python-version", "lab"]

    for key in expand_gh_matrix(matrix):
        yield tuple([key[k] for k in keys])
