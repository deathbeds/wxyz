""" Isomorphic widgets for parsing and dumping YAML
"""

from ._version import __version__  # noqa
from .widget_yaml import YAML, UnYAML

__all__ = ["__version__", "YAML", "UnYAML"]
