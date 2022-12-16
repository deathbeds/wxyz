""" paths, versions and other metadata for wxyz

"""
# pylint: disable=too-few-public-methods
import json
import os
import platform
import shutil
import site
import sys
from pathlib import Path

import jinja2
import yaml

try:
    import tomllib
except ImportError:
    import tomli as tomllib


try:
    from colorama import init

    init()
except ImportError:
    pass

RUNNING_IN_CI = bool(json.loads(os.environ.get("RUNNING_IN_CI", "false")))
RUNNING_IN_BINDER = bool(json.loads(os.environ.get("RUNNING_IN_BINDER", "false")))

# avoid certain checks etc
BUILDING_IN_CI = bool(json.loads(os.environ.get("BUILDING_IN_CI", "false")))

# generally avoid re-building assetc, checks.
TESTING_IN_CI = bool(json.loads(os.environ.get("TESTING_IN_CI", "false")))

RUNNING_IN_GITHUB = bool(json.loads(os.environ.get("RUNNING_IN_GITHUB", "false")))

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
LERNA_EXEC = [JLPM, "lerna", "exec", "--stream"]
LAB_EXT = ["jupyter", "labextension"]

PY_VER = "".join(map(str, sys.version_info[:2]))

LICENSE_NAME = "LICENSE.txt"

SCRIPTS = Path(__file__).parent
ROOT = SCRIPTS.parent

BUILD = ROOT / "build"
OK = BUILD / "ok"

GITHUB = CI = ROOT / ".github"
CI_YML = GITHUB / "workflows" / "ci.yml"
CI_YML_DATA = yaml.safe_load(CI_YML.read_text(encoding="utf-8"))
CI_TEST_MATRIX = CI_YML_DATA["jobs"]["test"]["strategy"]["matrix"]
LOCKS = GITHUB / "locks"
REQS = GITHUB / "reqs"

ALL_CONDA_PLATFORMS = ["linux-64", "osx-64", "win-64"]
LOCK_PY = "3.11"

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
    WXYZ = REQS.glob("wxyz_*.yml")


SRC = ROOT / "src"
PY_SRC = SRC
DOCS = ROOT / "docs"
DOCS_CONF_PY = DOCS / "conf.py"
DOCS_TEMPLATES = (DOCS / "_templates").rglob("*.html")
DOCS_IPYNB = [nb for nb in DOCS.rglob("*.ipynb") if "ipynb_checkpoints" not in str(nb)]
DOCS_STATIC = DOCS / "_static"
DOCS_LOGO = DOCS_STATIC / "wxyz.svg"
DOCS_FAVICON = DOCS_STATIC / "favicon.ico"
DODO = ROOT / "dodo.py"

PYLINTRC = ROOT / ".pylintrc"

SRC_IGNORE_PATTERNS = [
    "/.ipynb_checkpoints/",
    "/build/",
    "/dist/",
    "/lib/",
    "/node_modules/",
    "/*.egg-info/",
    "/output/",
    "/_d/",
]
# these are actual packages
ALL_PYPROJECT_TOML = sorted(PY_SRC.glob("*/pyproject.toml"))
ALL_SRC_PY = sorted(
    [
        py
        for py in PY_SRC.rglob("*.py")
        if all(p not in str(py.as_posix()) for p in SRC_IGNORE_PATTERNS)
    ]
)
ALL_PY = sorted([DODO, *SCRIPTS.glob("*.py"), *ALL_SRC_PY, DOCS_CONF_PY])
ALL_YAML = sorted([*REQS.rglob("*.yml"), *CI.rglob("*.yml")])
ALL_MD = sorted(ROOT.glob("*.md"))

DIST = ROOT / "dist"

TEST_OUT = BUILD / "test_output"
DOCS_OUT = BUILD / "docs"
DOCS_BUILDINFO = DOCS_OUT / ".buildinfo"


def NO_SPELL():
    """files we don't spell/link check"""
    return sorted(
        set(
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
    )


def ALL_DOC_HTML():
    """all the generated HTML"""
    return sorted(DOCS_OUT.rglob("*.html"))


def ALL_SPELL_DOCS():
    """files we do spell/link check"""
    no_spell = NO_SPELL()
    return [p for p in ALL_DOC_HTML() if p not in no_spell]


SPELL_LANGS = "en-GB,en_US"
DICTIONARY = DOCS / "dictionary.txt"
ROBOT_OUT = TEST_OUT / "robot"

ATEST = ROOT / "atest"
ATEST_OUT = ATEST / "output"
ATEST_PY = sorted(ATEST.rglob("*.py"))

PY_PROJ = {p: tomllib.loads(p.read_text(encoding="utf-8")) for p in ALL_PYPROJECT_TOML}
PY_VERSION = {ppt: pptd["project"]["version"] for ppt, pptd in PY_PROJ.items()}
PY_DEV_REQS = BUILD / "requirements-dev.txt"

PY_DOCS_DOT = [
    DOCS / "widgets/dot" / f"""classes_{ppt.parent.name.replace("wxyz_", "")}.dot"""
    for ppt in PY_PROJ
]
PY_DOCS_RST = [
    DOCS / f"""widgets/{ppt.parent.name.replace("wxyz_", "")}.rst""" for ppt in PY_PROJ
]


DOCS_DOT = [*PY_DOCS_DOT]

SITE_PKGS = Path(site.getsitepackages()[0])

YARN_LOCK = ROOT / "yarn.lock"
YARN_INTEGRITY = ROOT / "node_modules" / ".yarn-integrity"
ROOT_PACKAGE = ROOT / "package.json"

PACKAGES = ROOT / "packages"
TS_PACKAGE = sorted(PACKAGES.glob("*/package.json"))

TS_SRC = [p.parent for p in TS_PACKAGE]
TS_READMES = [p / "README.md" for p in TS_SRC]
TS_LICENSES = [p / "LICENSE.txt" for p in TS_SRC]
TS_META = PACKAGES / "wxyz-meta"
TS_META_BUILD = PACKAGES / "wxyz-meta/lib/.tsbuildinfo"
TS_ALL_BUILD = [p / "lib" / ".tsbuildinfo" for p in TS_SRC]

WXYZ_LAB_EXTENSIONS = [tsp.parent for tsp in TS_PACKAGE if tsp.parent != TS_META]
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
    tsp.parent
    / f"""deathbeds-{tsp_json["name"].split("/")[-1]}-{tsp_json["version"]}.tgz"""
    for tsp, tsp_json in TS_PACKAGE_CONTENT.items()
]
TS_D_PACKAGE_JSON = {
    SRC
    / tsp_json["jupyterlab"]["discovery"]["server"]["base"]["name"]: (
        tsp.parent / tsp_json["jupyterlab"]["outputDir"] / "package.json"
    ).resolve()
    for tsp, tsp_json in TS_PACKAGE_CONTENT.items()
    if "jupyterlab" in tsp_json
}

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
LICENSE = ROOT / LICENSE_NAME

ALL_MD = sorted(
    set(
        [
            *PY_SRC.rglob("*.md"),
            *ROOT.glob("*.md"),
            CONTRIBUTING,
            README,
        ]
    )
)

ALL_PRETTIER = sorted(
    {
        pretty
        for pretty in [
            *ALL_MD,
            *ALL_YAML,
            *CI.glob("*.yml"),
            *DOCS.rglob("*.css"),
            *ROOT.glob("*.json"),
            *ROOT.glob("*.yml"),
            *SRC.rglob("*.css"),
            *SRC.rglob("*.json"),
            *SRC.rglob("*.ts"),
            *SRC.rglob("*.yml"),
        ]
        if all(p not in str(pretty.as_posix()) for p in SRC_IGNORE_PATTERNS)
    }
)

ALL_ROBOT = [*ATEST.rglob("*.robot")]

PY_README_TXT = """
# `{{ project.name }}`

[![pypi-badge][]][pypi]{% if js_pkg %} [![npm-badge][]][npm]{% endif
%} [![docs-badge][docs]]

[docs-badge]: https://img.shields.io/badge/docs-pages-black
[docs]: https://wxyz.rtfd.io
[pypi-badge]: https://img.shields.io/pypi/v/{{ project.name }}
[pypi]: https://pypi.org/project/{{ project.name.replace("_", "-") }}
{% if js_pkg %}
[npm-badge]: https://img.shields.io/npm/v/{{ js_pkg.name }}
[npm]: https://www.npmjs.com/package/{{ js_pkg.name }}
{% endif %}

> {{ project.description }}

## Installation

> Prerequisites:
> - `python {{ project["requires-python"] }}`
> - `jupyterlab >=3.1,<4`

```bash
pip install {{ project.name }}
```
"""

PY_README_TMPL = jinja2.Template(PY_README_TXT.strip())

TS_README_TXT = """
# `{{ name }}`

{% set py = jupyterlab.discovery.server.base.name %}

[![pypi-badge][]][pypi] [![npm-badge][]][npm] [![docs-badge][docs]]

[pypi-badge]: https://img.shields.io/pypi/v/{{ py }}
[pypi]: https://pypi.org/project/{{ py.replace("_", "-") }}
[npm-badge]: https://img.shields.io/npm/v/{{ name }}
[npm]: https://www.npmjs.com/package/{{ name }}
[docs-badge]: https://img.shields.io/badge/docs-pages-black
[docs]: https://wxyz.rtfd.io

> {{ description }}

**If you just want to _use_ `{{ name }}` in JupyterLab 3**

```bash
pip install {{ py }}  # or conda, or mamba
```

## Developer Installation

The public API of the widgets in `{{ name }}` are not yet fully documented.
However, it's likely that you can:

```bash
jlpm add {{ name }}
```

and then, in your widget extension:

```ts
import wxyz from '{{ name }}';

console.log(wxyz); // and see _something_
```

## Legacy Installation (Pre-JupyterLab 2)

> _This approach is no longer recommended, and is **not tested**_

> Prerequisites:
> - `python >=3.8`
> - `nodejs >=18`
> - `jupyterlab >=3.1,<4`

```bash
jupyter labextension install @jupyter-widgets/jupyterlab-manager
{%- for dep in devDependencies -%}
{% if "@deathbeds" in dep %} {{ dep }}{% endif %}
{%- endfor %} {{ name }}
pip install {{ jupyterlab.discovery.server.base.name }}
```
"""

TS_README_TMPL = jinja2.Template(TS_README_TXT.strip())

ALL_VERSION_PY = sorted(SRC.glob("*/src/wxyz/*/_version.py"))

PY_VERSION_TXT = '''
"""source of truth for {{ project["name"] }} version info"""
from importlib.metadata import version

{% if js_pkg %}
import sys
from pathlib import Path

module_name = "{{ js_pkg["name"] }}"
module_version = "{{ js_pkg["version"] }}"

HERE = Path(__file__).parent

IN_TREE = (HERE / f"../_d/share/jupyter/labextensions/{module_name}").resolve()
IN_PREFIX = Path(sys.prefix) / f"share/jupyter/labextensions/{module_name}"

__prefix__ = IN_TREE if IN_TREE.exists() else IN_PREFIX
{% endif %}

NAME = "{{ project["name"] }}"
__version__ = version(NAME)
'''

PY_VERSION_TMPL = jinja2.Template(PY_VERSION_TXT.strip())


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
    ppt.parent.name: sorted((ppt.parent / "src").rglob("*.py")) for ppt in PY_PROJ
}

LINT_GROUPS["misc"] = [DODO, *SCRIPTS.glob("*.py"), *ATEST_PY, DOCS_CONF_PY]

SCHEMA = BUILD / "schema"

# these schema update files in-place


SCHEMA_TS_CM_OPTIONS = PACKAGES / "wxyz-lab/src/widgets/_cm_options.ts"

SCHEMA_TS_DG_STYLE = PACKAGES / "wxyz-datagrid/src/widgets/_datagrid_styles.ts"

SCHEMA_WIDGETS = {
    SCHEMA_TS_CM_OPTIONS: [
        PACKAGES / "wxyz-lab/src/widgets/editor.ts",
        SRC / "wxyz_lab/src/wxyz/lab/widget_editor.py",
    ],
    SCHEMA_TS_DG_STYLE: [
        PACKAGES / "wxyz-datagrid/src/widgets/pwidgets/stylegrid.ts",
        SRC / "wxyz_datagrid/src/wxyz/datagrid/widget_stylegrid.py",
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
