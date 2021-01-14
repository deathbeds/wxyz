""" Lumino DataGrid widgets powered by pandas and JSON Table Schema
"""
from ._version import __version__, module_name
from .widget_datagrid import DataGrid
from .widget_selectgrid import SelectGrid
from .widget_stylegrid import (
    CellRenderer,
    FixedFunc,
    FormatFunc,
    GridStyle,
    StyleGrid,
    TextRenderer,
)

__all__ = [
    "__version__",
    "CellRenderer",
    "DataGrid",
    "FixedFunc",
    "FormatFunc",
    "GridStyle",
    "SelectGrid",
    "StyleGrid",
    "TextRenderer",
]


def _jupyter_labextension_paths():
    return [{"src": "labextension", "dest": module_name}]
