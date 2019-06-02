import subprocess
import sys

from . import ROOT, PY_SRC, _run, PY, DIST

"""
|-
cd packages/ipywxyz \
&& python setup.py sdist --dist-dir $PROJECT_DIR/dist/sdist \
&& cd $PROJECT_DIR \
&& conda-build -c conda-forge --output-folder dist/conda-bld conda.recipe
"""

if __name__ == "__main__":
    for pkg in PY_SRC.glob("wxyz_*"):
        _run([PY, "setup.py", "sdist", "--dist-dir", DIST / "sdist"], cwd=str(pkg))
    _run([
        "conda", "build", "-c", "conda-forge", ".", "--output-folder", DIST / "conda-bld",
        "--skip-existing"
    ], cwd=ROOT / "recipes")
