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
