# wxyz

> has nothing to do with wx

[![binder-badge][]][binder] | [ROADMAP][] | [EXAMPLES][] | [CONTRIBUTING][]

Try to bring more isomorphic capabilities to the Jupyter Widget stack.

|    `from wxyz.X` | `import Y`                                                                 |     Python | Browser               |
| ---------------: | :------------------------------------------------------------------------- | ---------: | :-------------------- |
|             core | **JSON**<br/>**UnJSON**                                                    |       json | JSON                  |
|             core | **JSONSchema**                                                             | jsonschema | ajv                   |
|         datagrid | **DataGrid**<br/>**StyleGrid**<br/>**SelectGrid**                          |     pandas | Lumino                |
|              lab | **DockBox**<br/>**DockPop**                                                |          - | Lumino                |
|              lab | **Editor**                                                                 |          - | CodeMirror            |
|              lab | **Markdown**                                                               |    mistune | marked                |
| json_schema_form | **JSONSchemaForm**                                                         |          - | react-jsonschema-form |
|           jsonld | **Compact**<br/>**Expand**<br/>**Flatten**<br/>**Frame**<br/>**Normalize** |       pyld | jsonld.js             |
|        tpl_jinja | **Template**                                                               |     jinja2 | nunjucks              |
|             yaml | **YAML**                                                                   |     pyyaml | js-yaml               |

[binder]: https://mybinder.org/v2/gh/deathbeds/wxyz/master?urlpath=lab/tree/src/py/wxyz_notebooks/src/wxyz/notebooks/index.ipynb
[binder-badge]: https://mybinder.org/badge_logo.svg
[roadmap]: ./ROADMAP.md
[examples]: ./src/py/wxyz_notebooks/src/wxyz/notebooks/index.ipynb
[contributing]: ./CONTRIBUTING.md
