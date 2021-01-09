""" Widgets for working with JSON Schema interactively
"""
# pylint: disable=no-self-use,redefined-builtin

from .base import JSONSchemaFormBase, T, W


@W.register
class JSONSchemaForm(JSONSchemaFormBase, W.Box):
    """Show a form based on an JSON Schema (and/or UI schema)"""

    _model_name = T.Unicode("JSONSchemaFormModel").tag(sync=True)
    _view_name = T.Unicode("JSONSchemaFormView").tag(sync=True)

    value = T.Any(allow_none=True).tag(sync=True)
    schema = T.Dict(allow_none=True).tag(sync=True)
    ui_schema = T.Dict(allow_none=True).tag(sync=True)
    errors = T.List().tag(sync=True)
