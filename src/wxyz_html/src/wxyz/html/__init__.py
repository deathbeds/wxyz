""" Widgets for core HTML 5 controls
"""
from ._version import __prefix__, __version__, module_name
from .widget_color import AlphaColor, AlphaColorPicker, EmptyAlphaColor
from .widget_file import File, FileBox, JSONFile, TextFile
from .widget_fullscreen import Fullscreen

__all__ = [
    "_jupyter_labextension_paths",
    "__version__",
    "AlphaColor",
    "AlphaColorPicker",
    "EmptyAlphaColor",
    "File",
    "FileBox",
    "Fullscreen",
    "JSONFile",
    "TextFile",
]


def _jupyter_labextension_paths():
    return [dict(src=str(__prefix__), dest=module_name)]
