""" Isomorphic JSON widgets
"""
from ._version import __prefix__, __version__, module_name
from .base import Fn
from .widget_json import JSON, JSONPointer, JSONSchema, UnJSON

__all__ = [
    "_jupyter_labextension_paths",
    "__version__",
    "Fn",
    "UnJSON",
    "JSON",
    "JSONPointer",
    "JSONSchema",
]


def _jupyter_labextension_paths():
    return [dict(src=str(__prefix__), dest=module_name)]
