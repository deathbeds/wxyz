# `@deathbeds/wxyz-core`

[![pypi-badge][]][pypi] [![npm-badge][]][npm] [![docs-badge][docs]]

[pypi-badge]: https://img.shields.io/pypi/v/wxyz_core
[pypi]: https://pypi.org/project/wxyz-core
[npm-badge]: https://img.shields.io/npm/v/@deathbeds/wxyz-core
[npm]: https://www.npmjs.com/package/@deathbeds/wxyz-core
[docs-badge]: https://img.shields.io/badge/docs-pages-black
[docs]: https://deathbeds.github.io/wxyz

> Experimental Jupyter widgets for JSON and evented transformations

**If you just want to _use_ `@deathbeds/wxyz-core` in JupyterLab 3**

```bash
pip install wxyz_core  # or conda, or mamba
```

## Developer Installation

The public API of the widgets in `@deathbeds/wxyz-core` are not yet fully documented.
However, it's likely that you can:

```bash
jlpm add @deathbeds/wxyz-core
```

and then, in your widget extension:

```ts
import wxyz from '@deathbeds/wxyz-core';

console.log(wxyz); // and see _something_
```

## Legacy Installation (Pre-JupyterLab 2)

> _This approach is no longer recommended, and is **not tested**_

> Prerequisites:
>
> - `python >=3.6`
> - `nodejs >=12`
> - `jupyterlab >=3,<4`

```bash
jupyter labextension install @jupyter-widgets/jupyterlab-manager @deathbeds/wxyz-core
pip install wxyz_core
```

---

# wxyz

> Experimental [Widgets][] for [JupyterLab][].

|           build           |            demo             |                            docs                            |
| :-----------------------: | :-------------------------: | :--------------------------------------------------------: |
| [![build-badge][]][build] | [![binder-badge][]][binder] | [DOCS][] — [EXAMPLES][] — [CHANGELOG][] — [CONTRIBUTING][] |

## Install and Use

| `pip or conda install W` |      `from wxyz.Y` | `import Z`                                                                                 | _powered by_                               |
| :----------------------- | -----------------: | :----------------------------------------------------------------------------------------- | ------------------------------------------ |
| `wxyz_core`              |             `core` | `JSON`<br/>`UnJSON`<br/>                                                                   | `jsonpointer`<br/>`jsonschema`             |
| `wxyz_datagrid`          |         `datagrid` | `DataGrid`<br/>`GridStyle`<br/>`SelectGrid`<br/>`StyleGrid`                                | `pandas`<br/>`wxyz_core`                   |
| `wxyz_html`              |             `html` | `AlphaColorPicker`<br/>`File`<br/>`FileBox`<br/>`FullScreen`<br/>`JSONFile`<br/>`TextFile` | `wxyz_core`                                |
| `wxyz_dvcs`              |             `dvcs` | `repos.repo_git.Git`<br/>`Watcher`                                                         | `gitpython`<br/>`watchgod`<br/>`wxyz_core` |
| `wxyz_json_e`            |           `json_e` | `JSONE`                                                                                    | `jsone`<br/>`wxyz_core`                    |
| `wxyz_json_schema_form`  | `json_schema_form` | `JSONSchemaForm`                                                                           | `wxyz_core`                                |
| `wxyz_jsonld`            |           `jsonld` | `Compact`<br/>`Expand`<br/>`Flatten`<br/>`Frame`<br/>`Normalize`                           | `pyld`<br/>`wxyz_core`                     |
| `wxyz_lab`               |              `lab` | `DockBox`<br/>`DockPop`<br/>`Editor`<br/>`Markdown`<br/>`Terminal`<br/>`ModeInfo`          | `jupyterlab`<br/>`wxyz_core`               |
| `wxyz_svg`               |              `svg` | `SVGBox`                                                                                   | `wxyz_core`                                |
| `wxyz_tpl_jinja`         |        `tpl_jinja` | `Template`                                                                                 | `jinja2`<br/>`wxyz_core`                   |
| `wxyz_yaml`              |             `yaml` | `YAML`                                                                                     | `pyyaml`<br/>`wxyz_core`                   |

### Strongly Discouraged

`wxyz_notebooks`, not **recommended for production use**, requires all of the
`wxyz_*` packages.

Some _`extra(s)` dangerous_ dependencies are available as well

```bash
pip install wxyz_notebooks              # wxyz_*
pip install wxyz_notebooks[binder]      # everything used on binder demos, used in tests
pip install wxyz_notebooks[thirdparty]  # some casually co-tested third-party packages
pip install wxyz_notebooks[all]         # everything. it's a lot. good luck.
```

It is unknown whether the heavier dependencies will continue to work in the future
and may carry _very specific version pins_ which might not be solveable with any old:

- operating system
- version of python
- package manager

## Motivation

`wxyz` contains a number of "missing pieces" from the [ipywidgets][] toolbox.
It is made up of a number of packages for Python and the browser, in [this repo][].
While many create _pixels on the page_, some are focused around configurably
transforming the [traitlets][] of one widget to another, in the _kernel_, the
_browser_ or _both_.

## Uninstall

We're sad to see you go!

Use `pip` or `conda` to uninstall any `wxyz_*` packages.

## Alternatives

If you don't like `wxyz`, that's fine! There are a number of related tools that
might be better suited to your needs.

- [formulas]
  - a python-side re-implementation of an Excel/LibreOffice reactive functional
    programming model
- [ipyevents]
  - fine-grained DOM event control
- [ipylab]
  - a number of similar utilities as parts of `wxyz.lab`, and nice
    support for commands, and additional [lumino][] primitives, e.g. `SplitPanel`
- [ipyregulartable]
  - a high-performance datagrid solution, supporting pandas `MultiIndex`-type
    data
- [jupyter-starters]
  - wizard-style project templates, driven by simple configuration, JSON Schema
    or notebooks
- [jupyterlab-tour]
  - a pleasant "guided tour" of JupyterLab via CSS selectors and JSON Schema

[binder-badge]: https://mybinder.org/badge_logo.svg
[binder]: https://mybinder.org/v2/gh/deathbeds/wxyz/master?urlpath=lab/tree/src/py/wxyz_notebooks/src/wxyz/notebooks/index.ipynb
[docs]: https://deathbeds.github.io/wxyz
[build-badge]: https://dev.azure.com/nickbollweg/deathbeds/_apis/build/status/deathbeds.wxyz?branchName=master
[build]: https://dev.azure.com/nickbollweg/deathbeds/_build/latest?definitionId=6&branchName=master
[changelog]: https://github.com/deathbeds/wxyz/blob/master/CHANGELOG.md
[contributing]: https://github.com/deathbeds/wxyz/blob/master/CONTRIBUTING.md
[examples]: https://github.com/deathbeds/wxyz/blob/master/src/py/wxyz_notebooks/src/wxyz/notebooks/index.ipynb
[formulas]: https://pypi.org/project/formulas/
[ipyevents]: https://github.com/mwcraig/ipyevents
[ipylab]: https://github.com/jtpio/ipylab
[ipyregulartable]: https://github.com/jpmorganchase/ipyregulartable
[ipywidgets]: https://github.com/jupyter-widgets/ipywidgets
[jupyter-starters]: https://pypi.org/project/jupyter-starters/
[jupyterlab-tour]: https://github.com/fcollonval/jupyterlab-tour
[jupyterlab]: https://github.com/jupyterlab/jupyterlab
[lumino]: https://github.com/jupyterlab/lumino
[this repo]: https://github.com/deathbeds/wxyz
[traitlets]: https://github.com/ipython/traitlets
[widgets]: https://jupyter.org/widgets
