""" paths, versions and other metadata for wxyz
"""
# pylint: disable=too-few-public-methods
import json
import os
import platform
import re
import site
import sys
from pathlib import Path

try:
    from yaml import safe_load
except ImportError:
    from ruamel_yaml import safe_load


RUNNING_IN_CI = bool(json.loads(os.environ.get("RUNNING_IN_CI", "false")))
RUNNING_IN_BINDER = bool(json.loads(os.environ.get("RUNNING_IN_BINDER", "false")))

PY = Path(sys.executable)
PYM = [PY, "-m"]
PIP = [*PYM, "pip"]
JPY = [*PYM, "jupyter"]
OS = platform.system()

WIN = OS == "Windows"
OSX = OS == "Darwin"
LINUX = OS == "Linux"

CONDA_PLATFORM = "win-64" if WIN else "osx-64" if OSX else "linux-64"

CONDA_CMD = "conda" if WIN else "mamba"

PY_VER = "".join(map(str, sys.version_info[:2]))

SCRIPTS = Path(__file__).parent
ROOT = SCRIPTS.parent

BUILD = ROOT / "build"
OK = BUILD / "ok"

CI = ROOT / "ci"
PIPELINES = ROOT / "azure-pipelines.yml"
CI_TEST_YML = CI / "job.test.yml"
CI_TEST_MATRIX = safe_load(CI_TEST_YML.read_text())["parameters"]
LOCKS = CI / "locks"
REQS = ROOT / "reqs"
RECIPES = ROOT / "recipes"

ALL_CONDA_PLATFORMS = ["linux-64", "osx-64", "win-64"]


class ENV:
    """some partial conda environment descriptions"""

    atest = REQS / "atest.yml"
    base = REQS / "base.yml"
    binder = REQS / "binder.yml"
    lint = REQS / "lint.yml"
    lock = REQS / "lock.yml"
    utest = REQS / "utest.yml"
    win = REQS / "win.yml"
    unix = REQS / "unix.yml"
    tpot = REQS / "tpot.yml"
    WXYZ = REQS.glob("wxyz_*.yml")


SRC = ROOT / "src"
PY_SRC = SRC / "py"
TS_SRC = SRC / "ts"
DODO = ROOT / "dodo.py"

PYLINTRC = ROOT / ".pylintrc"

ALL_SETUP_CFG = sorted(PY_SRC.rglob("setup.cfg"))
ALL_SRC_PY = sorted([*PY_SRC.rglob("*.py")])
ALL_PY = sorted([DODO, *SCRIPTS.glob("*.py"), *ALL_SRC_PY])
ALL_YAML = sorted([*REQS.rglob("*.yml"), *CI.rglob("*.yml")])
ALL_MD = sorted([*ROOT.glob("*.md")])

DIST = ROOT / "dist"
IPYNB_HTML = DIST / "notebooks"

TEST_OUT = DIST / "test_output"
ROBOT_OUT = TEST_OUT / "robot"
LAB = ROOT / "lab"

ATEST = ROOT / "atest"
ATEST_OUT = ATEST / "output"
ATEST_PY = [*ATEST.rglob("*.py")]

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
LABEXT_TXT = ROOT / "labex.txt"
THIRD_PARTY_EXTENSIONS = sorted(
    [
        line.strip()
        for line in LABEXT_TXT.read_text().strip().splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
)
WXYZ_LAB_EXTENSIONS = [
    tsp.parent for tsp in TS_PACKAGE if "wxyz-meta" not in tsp.parent.name
]
ALL_LABEXTENSIONS = [*THIRD_PARTY_EXTENSIONS, *WXYZ_LAB_EXTENSIONS]
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

LAB_INDEX = LAB / "static" / "index.html"

CONDA_ORDER = ["core", "html", "lab", "datagrid", "svg", "tpl-jinja", "yaml"]

CONDA_BUILD_ARGS = [
    "conda-build",
    "-c",
    "conda-forge",
    "--output-folder",
    DIST / "conda-bld",
]

SDISTS = {
    pys.parent.name: DIST / "sdist" / f"{pys.parent.name}-{version}.tar.gz"
    for pys, version in PY_VERSION.items()
}

WHEELS = {
    pys.parent.name: DIST
    / "bdist_wheel"
    / f"{pys.parent.name}-{version}-py3-none-any.whl"
    for pys, version in PY_VERSION.items()
}


IPYNB = PY_SRC / "wxyz_notebooks" / "src" / "wxyz" / "notebooks"
DESIGN_IPYNB = IPYNB / "Design"

# this is duplicated in wxyz.notebook.tests
ALL_IPYNB = sorted(
    [
        ipynb
        for ipynb in IPYNB.rglob("*.ipynb")
        if ".ipynb_checkpoints" not in str(ipynb)
        and str(DESIGN_IPYNB) not in str(ipynb)
    ]
)

README = ROOT / "README.md"
CONTRIBUTING = ROOT / "CONTRIBUTING.md"

ALL_MD = sorted(
    set(
        [
            *PY_SRC.rglob("*.md"),
            *ROOT.glob("*.md"),
            *TS_SRC.rglob("*.md"),
            CONTRIBUTING,
            README,
        ]
    )
)

ALL_PRETTIER = sorted(
    [
        *CI.glob("*.yml"),
        *REQS.glob("*.yml"),
        *ROOT.glob("*.json"),
        *ROOT.glob("*.yml"),
        *TS_SRC.rglob("*.css"),
        *TS_SRC.rglob("*.json"),
        *TS_SRC.rglob("*.ts"),
        *TS_SRC.rglob("*.yml"),
        *ALL_YAML,
        *ALL_MD,
    ]
)

ALL_ROBOT = [*ATEST.rglob("*.robot")]
