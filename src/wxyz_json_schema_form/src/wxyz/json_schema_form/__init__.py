""" Isomorphic widget for working with JSON Schema
"""
from ._version import __version__, module_name
from .widget_json_schema_form import JSONSchemaForm

__all__ = ["__version__", "JSONSchemaForm"]


def _jupyter_labextension_paths():
    return [{"src": "labextension", "dest": module_name}]
