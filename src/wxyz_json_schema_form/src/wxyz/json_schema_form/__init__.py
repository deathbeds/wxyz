""" Isomorphic widget for working with JSON Schema
"""
from ._version import __prefix__, __version__, module_name
from .widget_json_schema_form import JSONSchemaForm

__all__ = ["_jupyter_labextension_paths", "__version__", "JSONSchemaForm"]


def _jupyter_labextension_paths():
    return [dict(src=str(__prefix__), dest=module_name)]
