""" Widgets for reusing parts of the JupyterLab interface
"""

from ._version import __prefix__, __version__, module_name
from .widget_dock import DockBox, DockPop
from .widget_editor import Editor, EditorConfig, EditorModeInfo
from .widget_markdown import Markdown
from .widget_term import Terminal

__all__ = [
    "_jupyter_labextension_paths",
    "__version__",
    "DockBox",
    "DockPop",
    "Editor",
    "Markdown",
    "Terminal",
    "EditorConfig",
    "EditorModeInfo",
]


def _jupyter_labextension_paths():
    return [dict(src=str(__prefix__), dest=module_name)]
