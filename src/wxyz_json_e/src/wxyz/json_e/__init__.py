""" experimental Jupyter widgets for JSON-E
"""

from ._version import __prefix__, __version__, module_name
from .widget_jsone import JSONE

__all__ = ["_jupyter_labextension_paths", "__version__", "JSONE"]


def _jupyter_labextension_paths():
    return [dict(src=str(__prefix__), dest=module_name)]
