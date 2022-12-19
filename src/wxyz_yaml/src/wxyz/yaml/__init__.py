""" Isomorphic widgets for parsing and dumping YAML
"""

from ._version import __prefix__, __version__, module_name
from .widget_yaml import YAML, UnYAML

__all__ = ["_jupyter_labextension_paths", "__version__", "YAML", "UnYAML"]


def _jupyter_labextension_paths():
    return [dict(src=str(__prefix__), dest=module_name)]
