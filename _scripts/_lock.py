""" environment locking for wxyz
"""
# pylint: disable=too-many-arguments,import-outside-toplevel

import subprocess
import tempfile
from pathlib import Path

from doit.tools import config_changed
from ruamel_yaml import safe_dump, safe_load

from . import _paths as P

# below here could move to a separate file

CHN = "channels"
DEP = "dependencies"


def make_lock_task(
    kind_, env_files, config, platform_, python_, nodejs_=None, lab_=None
):
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
            composite = merge(composite, safe_load(env_dep.read_text()))

        fake_deps = []

        if python_:
            fake_deps += [f"python ={python_}.*"]
        if nodejs_:
            fake_deps += [f"nodejs ={nodejs_}.*"]
        if lab_:
            fake_deps += [f"jupyterlab ={lab_}.*"]

        fake_env = {DEP: fake_deps}

        composite = merge(composite, fake_env)

        with tempfile.TemporaryDirectory() as td:
            tdp = Path(td)
            composite_yml = tdp / "composite.yml"
            composite_yml.write_text(safe_dump(composite, default_flow_style=False))
            print("composite\n\n", composite_yml.read_text(), "\n\n", flush=True)
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
            tmp_lock_txt = tmp_lock.read_text()
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


def iter_matrix(matrix):
    """generate"""
    for platform_ in matrix["platforms"]:
        for python_ in matrix["pythons"]:
            yield (
                platform_["condaPlatform"],
                python_["spec"],
                python_["nodejs"],
                python_["lab"],
            )
