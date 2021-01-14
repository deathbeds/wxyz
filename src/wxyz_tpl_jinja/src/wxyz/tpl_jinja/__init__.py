""" Isomorphic widget for rendering jinja2 templates
"""

from ._version import __version__, module_name
from .widget_template import Template

__all__ = ["__version__", "Template"]


def _jupyter_labextension_paths():
    return [{"src": "labextension", "dest": module_name}]
