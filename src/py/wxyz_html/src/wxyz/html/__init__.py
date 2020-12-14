""" Widgets for core HTML 5 controls
"""
from ._version import __version__  # noqa
from .widget_color import AlphaColor, AlphaColorPicker, EmptyAlphaColor
from .widget_file import File, FileBox
from .widget_fullscreen import Fullscreen

__all__ = [
    "__version__",
    "AlphaColor",
    "AlphaColorPicker",
    "EmptyAlphaColor",
    "File",
    "FileBox",
    "Fullscreen",
]
