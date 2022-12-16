""" Isomorphic widgets for working with JSON-LD algorithms
"""

from ._version import __prefix__, __version__, module_name
from .widget_jsonld import Compact, Expand, Flatten, Frame, Normalize

__all__ = [
    "_jupyter_labextension_paths",
    "__version__",
    "Expand",
    "Compact",
    "Flatten",
    "Frame",
    "Normalize",
]


def _jupyter_labextension_paths():
    return [dict(src=str(__prefix__), dest=module_name)]
