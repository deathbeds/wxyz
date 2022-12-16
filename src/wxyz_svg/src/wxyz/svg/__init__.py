""" Widget for working with SVG groups as a widget layout
"""

from ._version import __prefix__, __version__, module_name
from .widget_svg import SVGBox

__all__ = ["_jupyter_labextension_paths", "__version__", "SVGBox"]


def _jupyter_labextension_paths():
    return [dict(src=str(__prefix__), dest=module_name)]
