# `wxyz_lab`

> experimental Jupyter widgets for JupyterLab

## Installation

> Prerequisites:
>
> - `python >=3.6`
> - `nodejs >=10`
> - `jupyterlab >=2,<3`

```bash
pip install wxyz_lab
jupyter labextension install @jupyter-widgets/jupyterlab-manager @deathbeds/wxyz-core
```

---

# wxyz

> Experimental [Widgets][] for [JupyterLab][].

|           build           |            demo             |                           docs                           |
| :-----------------------: | :-------------------------: | :------------------------------------------------------: |
| [![build-badge][]][build] | [![binder-badge][]][binder] | [DOCS][] [EXAMPLES][] — [CHANGELOG][] — [CONTRIBUTING][] |

## Install and Use

| `pip install W`         | `jupyter labextension install X`   |      `from wxyz.Y` | `import Z`                                                                                 |
| :---------------------- | :--------------------------------- | -----------------: | :----------------------------------------------------------------------------------------- |
| `wxyz_core`             | `@deathbeds/wxyz-core`             |             `core` | `JSON`<br/>`UnJSON`<br/>                                                                   |
| `wxyz_datagrid`         | `@deathbeds/wxyz-datagrid`         |         `datagrid` | `DataGrid`<br/>`GridStyle`<br/>`SelectGrid`<br/>`StyleGrid`                                |
| `wxyz_html`             | `@deathbeds/wxyz-html`             |             `html` | `AlphaColorPicker`<br/>`File`<br/>`FileBox`<br/>`FullScreen`<br/>`JSONFile`<br/>`TextFile` |
| `wxyz_dvcs`             | `@deathbeds/wxyz-dvcs`             |             `dvcs` | `repos.repo_git.Git`<br/>`Watcher`                                                         |
| `wxyz_json_e`           | `@deathbeds/wxyz-json-e`           |           `json_e` | `JSONE`                                                                                    |
| `wxyz_json_schema_form` | `@deathbeds/wxyz-json-schema-form` | `json_schema_form` | `JSONSchemaForm`                                                                           |
| `wxyz_jsonld`           | `@deathbeds/wxyz-jsonld`           |           `jsonld` | `Compact`<br/>`Expand`<br/>`Flatten`<br/>`Frame`<br/>`Normalize`                           |
| `wxyz_lab`              | `@deathbeds/wxyz-lab`              |              `lab` | `DockBox`<br/>`DockPop`<br/>`Editor`<br/>`Markdown`<br/>`Terminal`<br/>`ModeInfo`          |
| `wxyz_svg`              | `@deathbeds/wxyz-svg`              |              `svg` | `SVGBox`                                                                                   |
| `wxyz_tpl_jinja`        | `@deathbeds/wxyz-tpl-nunjucks`     |        `tpl_jinja` | `Template`                                                                                 |
| `wxyz_yaml`             | `@deathbeds/wxyz-yaml`             |             `yaml` | `YAML`                                                                                     |

## Motivation

`wxyz` contains a number of "missing pieces" from the [ipywidgets][] toolbox.
It is made up of a number of packages for Python and the browser, in [this repo][].
While many create _pixels on the page_, some are focused around configurably
transforming the [traitlets][] of one widget to another, in the _kernel_, the
_browser_ or _both_.

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
