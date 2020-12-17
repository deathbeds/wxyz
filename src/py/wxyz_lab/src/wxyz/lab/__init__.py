""" Widgets for reusing parts of the JupyterLab interface
"""

from ._version import __version__
from .widget_dock import DockBox, DockPop
from .widget_editor import Editor, EditorConfig, EditorModeInfo
from .widget_markdown import Markdown
from .widget_term import Terminal

__all__ = [
    "__version__",
    "DockBox",
    "DockPop",
    "Editor",
    "Markdown",
    "Terminal",
    "EditorConfig",
    "EditorModeInfo",
]
