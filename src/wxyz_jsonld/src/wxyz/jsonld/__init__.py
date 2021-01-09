""" Isomorphic widgets for working with JSON-LD algorithms
"""

from ._version import __version__  # noqa
from .widget_jsonld import Compact, Expand, Flatten, Frame, Normalize

__all__ = ["__version__", "Expand", "Compact", "Flatten", "Frame", "Normalize"]
