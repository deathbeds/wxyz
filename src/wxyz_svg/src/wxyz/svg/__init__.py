""" Widget for working with SVG groups as a widget layout
"""

from ._version import __version__, module_name
from .widget_svg import SVGBox

__all__ = ["__version__", "SVGBox"]


def _jupyter_labextension_paths():
    return [{"src": "labextension", "dest": module_name}]
