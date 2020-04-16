import subprocess
import sys

from . import ROOT, PY_SRC, _run, PY, DIST


CONDA_ORDER = [
    "core",
    "html",
    "lab",
    "datagrid",
    "svg",
    "tpl-jjinja"
    "yaml"
]

CONDA_BUILD_ARGS = [
    "conda-build", "-c", "conda-forge", "--output-folder", DIST / "conda-bld",
]


if __name__ == "__main__":
    for pkg in PY_SRC.glob("wxyz_*"):
        for output in ["sdist", "bdist_wheel"]:
            _run([PY, "setup.py", output, "--dist-dir", DIST / output], cwd=str(pkg))

    if "--no-conda" not in sys.argv:
        try:
            _run([*CONDA_BUILD_ARGS, "--skip-existing", "."], cwd=ROOT / "recipes")
        except:
            for pkg in CONDA_ORDER:
                _run([*CONDA_BUILD_ARGS, f"wxyz-{pkg}"], cwd=ROOT / "recipes")
