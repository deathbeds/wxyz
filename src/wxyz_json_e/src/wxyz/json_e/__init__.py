""" experimental Jupyter widgets for JSON-E
"""

from ._version import __version__, module_name
from .widget_jsone import JSONE

__all__ = ["__version__", "JSONE"]


def _jupyter_labextension_paths():
    return [{"src": "labextension", "dest": module_name}]
