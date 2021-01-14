""" Isomorphic JSON widgets
"""
from ._version import __version__, module_name
from .base import Fn
from .widget_json import JSON, JSONPointer, JSONSchema, UnJSON

__all__ = ["__version__", "Fn", "UnJSON", "JSON", "JSONPointer", "JSONSchema"]


def _jupyter_labextension_paths():
    return [{"src": "labextension", "dest": module_name}]
