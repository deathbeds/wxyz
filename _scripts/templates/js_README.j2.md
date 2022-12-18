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
pip install {{ py }}
```

or...

```bash
mamba install -c conda-forge {{ py }}
```

or...

```bash
conda install -c conda-forge {{ py }}
```

## Developer Installation

The `{{ name }}` TypeScript API is documented on [ReadTheDocs][docs]. The contents of these docs are also available in-line in your editor, via the
`{{ name }}` on `npmjs.org` with:

- source maps
- TypeScript type definitions

It is encouraged to try working with it in a development setting:

```bash
jlpm add --dev {{ name }}
```

...and then, in your widget extension:

```ts
import wxyz from '{{ name }}';

console.log(wxyz); // and see _something_
```

## Reusing `{{ name }}`

### Packaging in Python

If you are authoring a pure-python widget, just ensure your package declares
a dependency on whatever leaf widgets you're using.

```toml
[project]
dependencies = [
    "{{ py }}",                     # but probably pinned sensibly
]
```

### Customizing in TypeScript

If you do use these widgets in _other_ widget extensions, you'll likely need to
ensure they are deduplicated by updating the `jupyterlab` key in your `package.json`:

```yaml
{
  "devDependencies": {
    "{{ name }}": "*"               # but probably pinned sensibly
  },
  "jupyterlab": {
    "sharedPackages": {
      "@jupyter-widgets/base": {
        "bundled": false,
        "singleton": true
      },
      "@jupyter-widgets/controls": {
        "bundled": false,
        "singleton": true
      },
      "{{ name }}": {
        "bundled": false,
        "singleton": true
      }
    }
  }
}
```
