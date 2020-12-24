""" paths, versions and other metadata for wxyz
"""
# pylint: disable=too-few-public-methods
import json
import os
import platform
import re
import shutil
import site
import sys
from pathlib import Path

import jinja2

try:
    import yaml
except ImportError:
    import ruamel_yaml as yaml


RUNNING_IN_CI = bool(json.loads(os.environ.get("RUNNING_IN_CI", "false")))
RUNNING_IN_BINDER = bool(json.loads(os.environ.get("RUNNING_IN_BINDER", "false")))
TESTING_IN_CI = bool(json.loads(os.environ.get("TESTING_IN_CI", "false")))

PY = Path(sys.executable)
PYM = [PY, "-m"]
PIP = [*PYM, "pip"]
JPY = [*PYM, "jupyter"]
OS = platform.system()

WIN = OS == "Windows"
OSX = OS == "Darwin"
LINUX = OS == "Linux"

CONDA_PLATFORM = "win-64" if WIN else "osx-64" if OSX else "linux-64"

CONDA_CMD = "mamba" if not WIN and shutil.which("mamba") else "conda"
JLPM = shutil.which("jlpm")

PY_VER = "".join(map(str, sys.version_info[:2]))

SCRIPTS = Path(__file__).parent
ROOT = SCRIPTS.parent

BUILD = ROOT / "build"
OK = BUILD / "ok"

CI = ROOT / "ci"
PIPELINES = ROOT / "azure-pipelines.yml"
CI_TEST_YML = CI / "job.test.yml"
CI_TEST_MATRIX = yaml.safe_load(CI_TEST_YML.read_text(encoding="utf-8"))["parameters"]
LOCKS = CI / "locks"
REQS = ROOT / "reqs"

ALL_CONDA_PLATFORMS = ["linux-64", "osx-64", "win-64"]

POSTBUILD = ROOT / ".binder" / "postBuild"


class ENV:
    """some partial conda environment descriptions"""

    atest = REQS / "atest.yml"
    base = REQS / "base.yml"
    binder = REQS / "binder.yml"
    docs = REQS / "docs.yml"
    lint = REQS / "lint.yml"
    lock = REQS / "lock.yml"
    utest = REQS / "utest.yml"
    win = REQS / "win.yml"
    unix = REQS / "unix.yml"
    tpot = REQS / "tpot.yml"
    unix_tpot = REQS / "unix_tpot.yml"
    win_tpot = REQS / "win_tpot.yml"
    WXYZ = REQS.glob("wxyz_*.yml")


SRC = ROOT / "src"
PY_SRC = SRC / "py"
TS_SRC = SRC / "ts"
DOCS = ROOT / "docs"
DOCS_CONF_PY = DOCS / "conf.py"
DOCS_TEMPLATES = (DOCS / "_templates").rglob("*.html")
DOCS_IPYNB = [nb for nb in DOCS.rglob("*.ipynb") if "ipynb_checkpoints" not in str(nb)]
DODO = ROOT / "dodo.py"

PYLINTRC = ROOT / ".pylintrc"

ALL_SETUP_CFG = sorted(PY_SRC.rglob("setup.cfg"))
ALL_SRC_PY = sorted(
    [
        py
        for py in PY_SRC.rglob("*.py")
        if ".ipynb_checkpoints" not in str(py) and "build" not in str(py)
    ]
)
ALL_PY = sorted([DODO, *SCRIPTS.glob("*.py"), *ALL_SRC_PY, DOCS_CONF_PY])
ALL_YAML = sorted([*REQS.rglob("*.yml"), *CI.rglob("*.yml")])
ALL_MD = sorted(ROOT.glob("*.md"))

DIST = ROOT / "dist"

TEST_OUT = BUILD / "test_output"
DOCS_OUT = BUILD / "docs"
DOCS_BUILDINFO = DOCS_OUT / ".buildinfo"
ALL_DOC_HTML = sorted(DOCS_OUT.rglob("*.html"))
NO_SPELL = sorted(
    [
        (DOCS_OUT / "search.html"),
        (DOCS_OUT / "gallery.html"),
        (DOCS_OUT / "genindex.html"),
        (DOCS_OUT / "py-modindex.html"),
        *(DOCS_OUT / "genindex").rglob("*.html"),
        *(DOCS_OUT / "_static").rglob("*.html"),
        *(DOCS_OUT / "_modules").rglob("*.html"),
        *(DOCS_OUT / "_sources").rglob("*.html"),
    ]
)
ALL_SPELL_DOCS = [p for p in ALL_DOC_HTML if p not in NO_SPELL]
SPELL_LANGS = "en-GB,en_US"
DICTIONARY = DOCS / "dictionary.txt"
ROBOT_OUT = TEST_OUT / "robot"
LAB = ROOT / "lab"

ATEST = ROOT / "atest"
ATEST_OUT = ATEST / "output"
ATEST_PY = sorted(ATEST.rglob("*.py"))

PY_SETUP = sorted(PY_SRC.glob("*/setup.py"))
PY_VERSION = {
    pys: re.findall(
        r"""__version__ = ["](.*)["]""",
        next((pys.parent / "src" / "wxyz").rglob("_version.py")).read_text(
            encoding="utf-8"
        ),
    )[0]
    for pys in PY_SETUP
}
PY_DEP = {
    pys.parent.name: [
        other.parent.name
        for other in PY_SETUP
        if pys.parent.name in (other.parent / "setup.cfg").read_text(encoding="utf-8")
        and pys != other
    ]
    for pys in PY_SETUP
}
PY_DEV_REQS = BUILD / "requirements-dev.txt"

PY_DOCS_DOT = [
    DOCS
    / "widgets"
    / "dot"
    / f"""classes_{py_setup.parent.name.replace("wxyz_", "")}.dot"""
    for py_setup in PY_SETUP
]
PY_DOCS_RST = [
    DOCS / "widgets" / f"""{py_setup.parent.name.replace("wxyz_", "")}.rst"""
    for py_setup in PY_SETUP
]


DOCS_DOT = [*PY_DOCS_DOT]

SITE_PKGS = Path(site.getsitepackages()[0])

YARN_LOCK = ROOT / "yarn.lock"
YARN_INTEGRITY = ROOT / "node_modules" / ".yarn-integrity"
ROOT_PACKAGE = ROOT / "package.json"
TS_PACKAGE = sorted(TS_SRC.glob("*/package.json"))
TS_READMES = sorted(TS_SRC.glob("*/README.md"))
TS_LICENSES = sorted(TS_SRC.glob("*/LICENSE.txt"))
LABEXT_TXT = ROOT / ".binder" / "labex.txt"
THIRD_PARTY_EXTENSIONS = sorted(
    [
        line.strip()
        for line in LABEXT_TXT.read_text(encoding="utf-8").strip().splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
)
WXYZ_LAB_EXTENSIONS = [
    tsp.parent for tsp in TS_PACKAGE if "wxyz-meta" not in tsp.parent.name
]
ALL_LABEXTENSIONS = [*THIRD_PARTY_EXTENSIONS, *WXYZ_LAB_EXTENSIONS]
ALL_TS = sorted(
    sum(
        [
            [*(tsp.parent / "src").rglob("*.ts"), *(tsp.parent / "style").rglob("*")]
            for tsp in TS_PACKAGE
        ],
        [],
    )
)
TS_PACKAGE_CONTENT = {
    tsp: json.loads(tsp.read_text(encoding="utf-8")) for tsp in TS_PACKAGE
}
TS_TARBALLS = [
    tsp.parent / f"""deathbeds-{tsp.parent.name}-{tsp_json["version"]}.tgz"""
    for tsp, tsp_json in TS_PACKAGE_CONTENT.items()
]


LAB_INDEX = LAB / "static" / "index.html"

SDISTS = {
    pys.parent.name: DIST / f"{pys.parent.name}-{version}.tar.gz"
    for pys, version in PY_VERSION.items()
}

WHEELS = {
    pys.parent.name: DIST / f"{pys.parent.name}-{version}-py3-none-any.whl"
    for pys, version in PY_VERSION.items()
}

HASH_DEPS = sorted([*TS_TARBALLS, *SDISTS.values(), *WHEELS.values()])
SHA256SUMS = DIST / "SHA256SUMS"

IPYNB = PY_SRC / "wxyz_notebooks" / "src" / "wxyz" / "notebooks"
DESIGN_IPYNB = IPYNB / "Design"

# this is duplicated in wxyz.notebook.tests
ALL_IPYNB = sorted(
    [
        ipynb
        for ipynb in sorted(IPYNB.rglob("*.ipynb"))
        if ".ipynb_checkpoints" not in str(ipynb)
        and str(DESIGN_IPYNB) not in str(ipynb)
    ]
)

WIDGET_LOG_OUT = BUILD / "nbwidgets"

README = ROOT / "README.md"
CONTRIBUTING = ROOT / "CONTRIBUTING.md"
LICENSE = ROOT / "LICENSE.txt"

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
    set(
        [
            *CI.glob("*.yml"),
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
)

ALL_ROBOT = [*ATEST.rglob("*.robot")]

PY_README_TXT = """
# `{{ metadata.name }}`

> {{ metadata.description }}

## Installation

> Prerequisites:
> - `python {{ options.python_requires }}`
> - `nodejs >=10`
> - `jupyterlab >=2,<3`
```bash
pip install {{ metadata.name }}
{%- if js_pkg %}
jupyter labextension install @jupyter-widgets/jupyterlab-manager
{%- for dep in js_pkg.devDependencies -%}
{% if "@deathbeds" in dep %} {{ dep }}{% endif %}
{%- endfor %} {{ name }}
{% endif %}```
"""

PY_README_TMPL = jinja2.Template(PY_README_TXT)

TS_README_TXT = """
# `{{ name }}`

> {{ description }}

## Installation

> Prerequisites:
> - `python >=3.6`
> - `nodejs >=10`
> - `jupyterlab >=2,<3`

```bash
jupyter labextension install @jupyter-widgets/jupyterlab-manager
{%- for dep in devDependencies -%}
{% if "@deathbeds" in dep %} {{ dep }}{% endif %}
{%- endfor %} {{ name }}
pip install {{ jupyterlab.discovery.server.base.name }}
```
"""

TS_README_TMPL = jinja2.Template(TS_README_TXT)


PY_LINT_CMDS = [
    {
        "black": lambda files: [
            ["isort", "--quiet", "--ac", *files],
            ["black", "--quiet", *files],
            ["git", "diff", "--color-words", "--", *files],
        ]
    },
    {
        "flake8": ["flake8", "--max-line-length", "88"],
        "pylint": ["pylint", "-sn", "-rn", f"--rcfile={PYLINTRC}"],
    },
]


LINT_GROUPS = {
    i.parent.name: [i, *sorted((i.parent / "src").rglob("*.py"))] for i in PY_SETUP
}

LINT_GROUPS["misc"] = [DODO, *SCRIPTS.glob("*.py"), *ATEST_PY, DOCS_CONF_PY]

SCHEMA = BUILD / "schema"
SCHEMA_WIDGETS = {
    TS_SRC
    / "wxyz-lab/src/widgets/_cm_options.ts": [
        TS_SRC / "wxyz-lab/src/widgets/editor.ts",
        PY_SRC / "wxyz_lab/src/wxyz/lab/widget_editor.py",
    ],
    TS_SRC
    / "wxyz-datagrid/src/widgets/_datagrid_styles.ts": [
        TS_SRC / "wxyz-datagrid/src/widgets/pwidgets/stylegrid.ts",
        PY_SRC / "wxyz_datagrid/src/wxyz/datagrid/widget_stylegrid.py",
    ],
}

PY_RST_TEMPLATE_TXT = """{{ stars }}
{{ module }}
{{ stars }}

.. currentmodule:: {{ module }}

.. automodule:: {{ module }}
   :members:
   :special-members:
   :inherited-members:
   :show-inheritance:
   :exclude-members: {{ exclude_members }}


Classes
-------

.. graphviz:: dot/classes_{{ name }}.dot
"""

PY_RST_TEMPLATE = jinja2.Template(PY_RST_TEMPLATE_TXT)

PYREVERSE = [
    "pyreverse",
    "--filter-mode=ALL",
    "--all-ancestors",
    "--module-names=y",
    # # we want widgets
    # "--ancestor", "ipywidgets.Widget",
    # # we want widgets
    # "--ancestor", "ipywidgets.Box"
]
