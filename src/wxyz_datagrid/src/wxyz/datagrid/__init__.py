""" Lumino DataGrid widgets powered by pandas and JSON Table Schema
"""
from ._version import __prefix__, __version__, module_name
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
    "_jupyter_labextension_paths",
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
    return [dict(src=str(__prefix__), dest=module_name)]
