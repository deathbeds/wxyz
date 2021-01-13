""" Isomorphic widgets for parsing and dumping YAML
"""

from ._version import __version__, module_name
from .widget_yaml import YAML, UnYAML


def _jupyter_labextension_paths():
    return [{"src": "labextension", "dest": module_name}]


__all__ = ["__version__", "YAML", "UnYAML"]
