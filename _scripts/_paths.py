""" paths, versions and other metadata for wxyz
"""
import json
import os
import re
import site
import sys
from pathlib import Path

RUNNING_IN_CI = os.environ.get("RUNNING_IN_CI") is not None

PY = Path(sys.executable)

SCRIPTS = Path(__file__).parent
ROOT = SCRIPTS.parent
SRC = ROOT / "src"
PY_SRC = SRC / "py"
TS_SRC = SRC / "ts"
DODO = ROOT / "dodo.py"
ALL_PY = sorted([DODO, *SCRIPTS.glob("*.py"), *PY_SRC.rglob("*.py")])


DIST = ROOT / "dist"
IPYNB = ROOT / "notebooks"
IPYNB_HTML = DIST / "notebooks"

TEST_OUT = DIST / "test_output"
ROBOT_OUT = TEST_OUT / "robot"
LAB = ROOT / "lab"

ATEST = ROOT / "atest"

CI = ROOT / "ci"

PY_SETUP = [*PY_SRC.glob("*/setup.py")]
PY_VERSION = {
    pys: re.findall(
        r"""__version__ = ["](.*)["]""",
        next((pys.parent / "src" / "wxyz").rglob("_version.py")).read_text(),
    )[0]
    for pys in PY_SETUP
}
SITE_PKGS = Path(site.getsitepackages()[0])

YARN_LOCK = ROOT / "yarn.lock"
YARN_INTEGRITY = ROOT / "node_modules" / ".yarn-integrity"
ROOT_PACKAGE = ROOT / "package.json"
TS_PACKAGE = [*TS_SRC.glob("*/package.json")]
ALL_TS = sum(
    [
        [*(tsp.parent / "src").rglob("*.ts"), *(tsp.parent / "style").rglob("*")]
        for tsp in TS_PACKAGE
    ],
    [],
)
TS_PACKAGE_CONTENT = {tsp: json.loads(tsp.read_text()) for tsp in TS_PACKAGE}
TS_TARBALLS = [
    tsp.parent / f"""deathbeds-{tsp.parent.name}-{tsp_json["version"]}.tgz"""
    for tsp, tsp_json in TS_PACKAGE_CONTENT.items()
]


CONDA_ORDER = ["core", "html", "lab", "datagrid", "svg", "tpl-jjinja", "yaml"]

CONDA_BUILD_ARGS = [
    "conda-build",
    "-c",
    "conda-forge",
    "--output-folder",
    DIST / "conda-bld",
]

WHEELS = [
    DIST / "bdist_wheel" / f"{pys.parent.name}-{version}-py3-none-any.whl"
    for pys, version in PY_VERSION.items()
]
