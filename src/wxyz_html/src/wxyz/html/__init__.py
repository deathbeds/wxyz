""" Widgets for core HTML 5 controls
"""
from ._version import __version__, module_name
from .widget_color import AlphaColor, AlphaColorPicker, EmptyAlphaColor
from .widget_file import File, FileBox, JSONFile, TextFile
from .widget_fullscreen import Fullscreen

__all__ = [
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
    return [{"src": "labextension", "dest": module_name}]
