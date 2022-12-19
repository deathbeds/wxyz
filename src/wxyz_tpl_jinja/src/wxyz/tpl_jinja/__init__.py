""" Isomorphic widget for rendering jinja2 templates
"""

from ._version import __prefix__, __version__, module_name
from .widget_template import Template

__all__ = ["_jupyter_labextension_paths", "__version__", "Template"]


def _jupyter_labextension_paths():
    return [dict(src=str(__prefix__), dest=module_name)]
