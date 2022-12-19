# `@deathbeds/wxyz-yaml`

[![pypi-badge][]][pypi] [![npm-badge][]][npm] [![docs-badge][docs]]

[pypi-badge]: https://img.shields.io/pypi/v/wxyz_yaml
[pypi]: https://pypi.org/project/wxyz-yaml
[npm-badge]: https://img.shields.io/npm/v/@deathbeds/wxyz-yaml
[npm]: https://www.npmjs.com/package/@deathbeds/wxyz-yaml
[docs-badge]: https://img.shields.io/badge/docs-pages-black
[docs]: https://wxyz.rtfd.io

> experimental Jupyter widgets for YAML

**If you just want to _use_ `@deathbeds/wxyz-yaml` in JupyterLab 3**

```bash
pip install wxyz_yaml
```

or...

```bash
mamba install -c conda-forge wxyz_yaml
```

or...

```bash
conda install -c conda-forge wxyz_yaml
```

## Developer Installation

The `@deathbeds/wxyz-yaml` TypeScript API is documented on [ReadTheDocs][docs]. The
contents of these docs are also available in-line in your editor, via the
`@deathbeds/wxyz-yaml` on `npmjs.org` with:

- source maps
- TypeScript type definitions

It is encouraged to try working with it in a development setting:

```bash
jlpm add --dev @deathbeds/wxyz-yaml
```

...and then, in your widget extension:

```ts
import wxyz from '@deathbeds/wxyz-yaml';

console.log(wxyz); // and see _something_
```

## Reusing `@deathbeds/wxyz-yaml`

### Packaging in Python

If you are authoring a pure-python widget, just ensure your package declares a
dependency on whatever leaf widgets you're using.

```toml
[project]
dependencies = [
    "wxyz_yaml",                     # but probably pinned sensibly
]
```

### Customizing in TypeScript

If you do use these widgets in _other_ widget extensions, you'll likely need to ensure
they are deduplicated by updating the `jupyterlab` key in your `package.json`:

```yaml
{ 'devDependencies': {
      '@deathbeds/wxyz-yaml': '*', # but probably pinned sensibly
    }, 'jupyterlab': { 'sharedPackages': { '@jupyter-widgets/base': { 'bundled': false, 'singleton': true }, '@jupyter-widgets/controls': { 'bundled': false, 'singleton': true }, '@deathbeds/wxyz-yaml': { 'bundled': false, 'singleton': true } } } }
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

`wxyz_notebooks`, not **recommended for production use**, requires all of the `wxyz_*`
packages.

Some _`extra(s)` dangerous_ dependencies are available as well

```bash
pip install wxyz_notebooks              # wxyz_*
pip install wxyz_notebooks[binder]      # everything used on binder demos, used in tests
pip install wxyz_notebooks[thirdparty]  # some casually co-tested third-party packages
pip install wxyz_notebooks[all]         # everything. it's a lot. good luck.
```

It is unknown whether the heavier dependencies will continue to work in the future and
may carry _very specific version pins_ which might not be solveable with any old:

- operating system
- version of python
- package manager

## Motivation

`wxyz` contains a number of "missing pieces" from the [ipywidgets][] toolbox. It is made
up of a number of packages for Python and the browser, in [this repo][]. While many
create _pixels on the page_, some are focused around configurably transforming the
[traitlets][] of one widget to another, in the _kernel_, the _browser_ or _both_.

## Uninstall

We're sad to see you go!

Use `pip` or `conda` to uninstall any `wxyz_*` packages.

## Alternatives

If you don't like `wxyz`, that's fine! There are a number of related tools that might be
better suited to your needs.

- [formulas]
  - a python-side re-implementation of an Excel/LibreOffice reactive functional
    programming model
- [ipyevents]
  - fine-grained DOM event control
- [ipylab]
  - a number of similar utilities as parts of `wxyz.lab`, and nice support for commands,
    and additional [lumino][] primitives, e.g. `SplitPanel`
- [ipyregulartable]
  - a high-performance datagrid solution, supporting pandas `MultiIndex`-type data
- [jupyter-starters]
  - wizard-style project templates, driven by simple configuration, JSON Schema or
    notebooks
- [jupyterlab-tour]
  - a pleasant "guided tour" of JupyterLab via CSS selectors and JSON Schema

[binder-badge]: https://mybinder.org/badge_logo.svg
[binder]:
  https://mybinder.org/v2/gh/deathbeds/wxyz/main?urlpath=lab/tree/src/py/wxyz_notebooks/src/wxyz/notebooks/index.ipynb
[docs]: https://deathbeds.github.io/wxyz
[build-badge]:
  https://dev.azure.com/nickbollweg/deathbeds/_apis/build/status/deathbeds.wxyz?branchName=main
[build]:
  https://dev.azure.com/nickbollweg/deathbeds/_build/latest?definitionId=6&branchName=main
[changelog]: https://github.com/deathbeds/wxyz/blob/main/CHANGELOG.md
[contributing]: https://github.com/deathbeds/wxyz/blob/main/CONTRIBUTING.md
[examples]:
  https://github.com/deathbeds/wxyz/blob/main/src/py/wxyz_notebooks/src/wxyz/notebooks/index.ipynb
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
