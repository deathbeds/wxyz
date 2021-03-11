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

try:
    import yaml
except ImportError:
    import ruamel_yaml as yaml

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

POSTBUILD = ROOT / ".binder" / "postBuild"


class ENV:
    """some partial conda environment descriptions"""

    atest = REQS / "atest.yml"
    base = REQS / "base.yml"
    binder = REQS / "binder.yml"
    docs = REQS / "docs.yml"
    future = REQS / "future.yml"
    lint = REQS / "lint.yml"
    lock = REQS / "lock.yml"
    tpot = REQS / "tpot.yml"
    unix = REQS / "unix.yml"
    unix_tpot = REQS / "unix_tpot.yml"
    utest = REQS / "utest.yml"
    win = REQS / "win.yml"
    win_tpot = REQS / "win_tpot.yml"
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
    ".ipynb_checkpoints/",
    "build/",
    "dist/",
    "lib/",
    "node_modules/",
    "*.egg-info/",
    "output/",
    "labextension/",
]
# these are actual packages
ALL_SETUP_CFG = sorted(PY_SRC.glob("*/setup.cfg"))
ALL_SRC_PY = sorted(
    [
        py
        for py in PY_SRC.rglob("*.py")
        if all([p not in str(py.as_posix()) for p in SRC_IGNORE_PATTERNS])
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

PY_SETUP = sorted(PY_SRC.glob("*/setup.py"))
PY_VERSION = {
    pys: json.loads(
        next((pys.parent / "src" / "wxyz").glob("*/js/package.json")).read_text(
            encoding="utf-8"
        )
    )["version"]
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

TS_PACKAGE = [[*(p.parent / "src").glob("wxyz/*/js/package.json")][0] for p in PY_SETUP]

TS_SRC = [p.parent for p in TS_PACKAGE]
TS_READMES = [p / "README.md" for p in TS_SRC]
TS_LICENSES = [p / "LICENSE.txt" for p in TS_SRC]
TS_META_BUILD = ROOT / "src/wxyz_notebooks/src/wxyz/notebooks/js/lib/.tsbuildinfo"
TS_ALL_BUILD = [p / "lib" / ".tsbuildinfo" for p in TS_SRC]

WXYZ_LAB_EXTENSIONS = [
    tsp.parent for tsp in TS_PACKAGE if "notebooks" not in tsp.parent.parent.name
]
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
        if all([p not in str(pretty.as_posix()) for p in SRC_IGNORE_PATTERNS])
    }
)

ALL_ROBOT = [*ATEST.rglob("*.robot")]

PY_README_TXT = """
# `{{ metadata.name }}`

[![pypi-badge][]][pypi]{% if js_pkg %} [![npm-badge][]][npm]{% endif
%} [![docs-badge][docs]]

[docs-badge]: https://img.shields.io/badge/docs-pages-black
[docs]: https://deathbeds.github.io/wxyz
[pypi-badge]: https://img.shields.io/pypi/v/{{ metadata.name }}
[pypi]: https://pypi.org/project/{{ metadata.name.replace("_", "-") }}
{% if js_pkg %}
[npm-badge]: https://img.shields.io/npm/v/{{ js_pkg.name }}
[npm]: https://www.npmjs.com/package/{{ js_pkg.name }}
{% endif %}

> {{ metadata.description }}

## Installation

> Prerequisites:
> - `python {{ options.python_requires }}`
> - `jupyterlab >=3,<4`

```bash
pip install {{ metadata.name }}
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
[docs]: https://deathbeds.github.io/wxyz

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
> - `python >=3.6`
> - `nodejs >=12`
> - `jupyterlab >=3,<4`

```bash
jupyter labextension install @jupyter-widgets/jupyterlab-manager
{%- for dep in devDependencies -%}
{% if "@deathbeds" in dep %} {{ dep }}{% endif %}
{%- endfor %} {{ name }}
pip install {{ jupyterlab.discovery.server.base.name }}
```
"""

TS_README_TMPL = jinja2.Template(TS_README_TXT.strip())


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

# these schema update files in-place


SCHEMA_TS_CM_OPTIONS = SRC / "wxyz_lab/src/wxyz/lab/js/src/widgets/_cm_options.ts"

SCHEMA_TS_DG_STYLE = (
    SRC / "wxyz_datagrid/src/wxyz/datagrid/js/src/widgets/_datagrid_styles.ts"
)

SCHEMA_WIDGETS = {
    SCHEMA_TS_CM_OPTIONS: [
        SRC / "wxyz_lab/src/wxyz/lab/js/src/widgets/editor.ts",
        SRC / "wxyz_lab/src/wxyz/lab/widget_editor.py",
    ],
    SCHEMA_TS_DG_STYLE: [
        SRC / "wxyz_datagrid/src/wxyz/datagrid/js/src/widgets/pwidgets/stylegrid.ts",
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


Classes
-------

.. graphviz:: dot/classes_{{ name }}.dot
"""

PY_RST_TEMPLATE = jinja2.Template(PY_RST_TEMPLATE_TXT)


PY_SETUP_TEXT = '''
"""generated setup for wxyz_{{ wxyz_name }}, do not edit by hand"""
import json
from pathlib import Path
WXYZ_NAME = "{{ wxyz_name }}"

HERE = Path(__file__).parent
JS_PKG = HERE / f"src/wxyz/{WXYZ_NAME}/js/package.json"

__jspackage__ = json.loads(JS_PKG.read_text(encoding="utf-8"))


HERE = Path(__file__).parent
EXT_NAME = __jspackage__["name"]

EXT_FILES = {}

SHARE = f"share/jupyter/labextensions/{EXT_NAME}"

EXT = HERE / f"src/wxyz/{WXYZ_NAME}/labextension"

for ext_path in [EXT] + [d for d in EXT.rglob("*") if d.is_dir()]:
    if ext_path == EXT:
        target = str(SHARE)
    else:
        target = f"{SHARE}/{ext_path.relative_to(EXT)}"
    EXT_FILES[target] = [
        str(p.relative_to(HERE).as_posix())
        for p in ext_path.glob("*")
        if not p.is_dir()
    ]

ALL_FILES = sum(EXT_FILES.values(), [])

assert (
    len([p for p in ALL_FILES if "remoteEntry" in str(p)]) == 1
), "expected _exactly one_ remoteEntry.*.js"

EXT_FILES[SHARE] += [f"src/wxyz/{WXYZ_NAME}/install.json"]

SETUP_ARGS=dict(
    version=__jspackage__["version"],
    data_files=[
        (str(k), list(map(str, v))) for k, v in EXT_FILES.items()
    ]
)

if __name__ == "__main__":
    import setuptools
    setuptools.setup(**SETUP_ARGS)
'''
PY_SETUP_TEMPLATE = jinja2.Template(PY_SETUP_TEXT.strip())


INSTALL_JSON_TEXT = """{
  "packageManager": "python",
  "packageName": "wxyz_{{ wxyz_name }}",
  "uninstallInstructions": "Use `pip/conda uninstall wxyz_{{ wxyz_name }}`"
}"""
INSTALL_JSON_TEMPLATE = jinja2.Template(INSTALL_JSON_TEXT.strip())

MANIFEST_TEXT = """
# generated python data file manifest for wxyz_{{ wxyz_name }}, do not edit by hand
include             README.md
include             src/wxyz/{{ wxyz_name }}/js/package.json
include             src/wxyz/{{ wxyz_name }}/js/LICENSE.txt
include             src/wxyz/{{ wxyz_name }}/js/README.md
recursive-include   src/wxyz/{{ wxyz_name }}/labextension *.*
global-exclude      .ipynb_checkpoints
global-exclude      node_modules
"""
MANIFEST_TEMPLATE = jinja2.Template(MANIFEST_TEXT.strip())

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
