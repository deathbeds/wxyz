# `wxyz_notebooks`

> notebook demos for experimental Jupyter widgets

## Installation

> Prerequisites:
>
> - `python >=3.6`
> - `nodejs >=10`
> - `jupyterlab >=2,<3`

````bash
pip install wxyz_notebooks```

---

# wxyz

> Experimental [Widgets][] for [JupyterLab][].

|           build           |            demo             |                      docs                       |
| :-----------------------: | :-------------------------: | :---------------------------------------------: |
| [![build-badge][]][build] | [![binder-badge][]][binder] | [EXAMPLES][] — [CHANGELOG][] — [CONTRIBUTING][] |

## Install and Use

| `pip install W`         | `jupyter labextension install X`   |      `from wxyz.Y` | `import Z`                                                         |
| :---------------------- | :--------------------------------- | -----------------: | :----------------------------------------------------------------- |
| `wxyz_core`             | `@deathbeds/wxyz-core`             |             `core` | `JSON`<br/>`UnJSON`<br/>                                           |
| `wxyz_datagrid`         | `@deathbeds/wxyz-datagrid`         |         `datagrid` | `DataGrid`<br/>`SelectGrid`<br/>`StyleGrid`                        |
| `wxyz_html`             | `@deathbeds/wxyz-html`             |             `html` | `AlphaColorPicker`<br/>`FileBox`<br/>`FullScreen`                  |
| `wyxz_dvcs`             |                                    |             `dvcs` | `repos.repo_git.Git`<br/>`Watcher`                                 |
| `wyxz_json_schema_form` | `@deathbeds/wxyz-json-schema-form` | `json_schema_form` | `JSONSchemaForm`                                                   |
| `wyxz_jsonld`           | `@deathbeds/wxyz-jsonld`           |           `jsonld` | `Compact`<br/>`Expand`<br/>`Flatten`<br/>`Frame`<br/>`Normalize`   |
| `wyxz_lab`              | `@deathbeds/wxyz-lab`              |              `lab` | `DockBox`<br/>`DockPop`<br/>`Editor`<br/>`Markdown`<br/>`Terminal` |
| `wyxz_svg`              | `@deathbeds/wxyz-svg`              |              `svg` | `SVGBox`                                                           |
| `wyxz_tpl_jinja`        | `@deathbeds/wxyz-tpl-nunjucks`     |        `tpl_jinja` | `Template`                                                         |
| `wyxz_yaml`             | `@deathbeds/wxyz-yaml`             |             `yaml` | `YAML`                                                             |

## Motivation

`wxyz` contains a number of "missing pieces" from the [ipywidgets][] toolbox.
It is made up of a number of packages for Python and the browser, in [this repo][].
While many create _pixels on the page_, some are focused around configurably
transforming the [traitlets][] of one widget to another, in the _kernel_, the
_browser_ or _both_.

[binder-badge]: https://mybinder.org/badge_logo.svg
[binder]: https://mybinder.org/v2/gh/deathbeds/wxyz/master?urlpath=lab/tree/src/py/wxyz_notebooks/src/wxyz/notebooks/index.ipynb
[build-badge]: https://dev.azure.com/nickbollweg/deathbeds/_apis/build/status/deathbeds.wxyz?branchName=master
[build]: https://dev.azure.com/nickbollweg/deathbeds/_build/latest?definitionId=6&branchName=master
[changelog]: https://github.com/deathbeds/wxyz/blob/master/CHANGELOG.md
[contributing]: https://github.com/deathbeds/wxyz/blob/master/CONTRIBUTING.md
[examples]: https://github.com/deathbeds/wxyz/blob/master/src/py/wxyz_notebooks/src/wxyz/notebooks/index.ipynb
[ipywidgets]: https://github.com/jupyter-widgets/ipywidgets
[jupyterlab]: https://github.com/jupyterlab/jupyterlab
[this repo]: https://github.com/deathbeds/wxyz
[traitlets]: https://github.com/ipython/traitlets
[widgets]: https://jupyter.org/widgets
````
