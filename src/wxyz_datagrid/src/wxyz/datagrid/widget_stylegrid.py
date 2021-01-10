""" A styled grid
"""
# pylint: disable=R0903,C0103,W0703,R0901
from wxyz.core.base import T, W
from wxyz.html import AlphaColor, EmptyAlphaColor

from ._version import module_name, module_version
from .base import DataGridBase
from .widget_datagrid import DataGrid


@W.register
class CellRenderer(DataGridBase):
    """``[0.1.6]/cellrenderer.ts#L29``"""

    _model_module = T.Unicode(module_name).tag(sync=True)
    _model_module_version = T.Unicode(module_version).tag(sync=True)
    _view_module = T.Unicode(module_name).tag(sync=True)
    _view_module_version = T.Unicode(module_version).tag(sync=True)
    _model_name = T.Unicode("CellRendererModel").tag(sync=True)

    region = T.Unicode("body").tag(sync=True)
    metadata = T.Dict().tag(sync=True)


@W.register
class FormatFunc(DataGridBase):
    """``[0.1.6]/textrenderer.ts#L308``"""

    _model_name = T.Unicode("FormatFuncModel").tag(sync=True)


@W.register
class TextRenderer(CellRenderer):
    """``[0.1.6]/textrenderer.ts#L21``"""

    _model_name = T.Unicode("TextRendererModel").tag(sync=True)

    format_func = T.Instance(FormatFunc, allow_none=True).tag(
        sync=True, **W.widget_serialization
    )

    background_color = EmptyAlphaColor("").tag(sync=True)
    font = T.Unicode("12px sans-serif").tag(sync=True)
    horizontal_alignment = T.Unicode("left").tag(sync=True)
    text_color = AlphaColor("#000000").tag(sync=True)
    vertical_alignment = T.Unicode("center").tag(sync=True)


@W.register
class FixedFunc(FormatFunc):
    """``[0.1.6]/textrenderer.ts#L365``"""

    _model_name = T.Unicode("FixedFuncModel").tag(sync=True)

    digits = T.Int().tag(sync=True)
    missing = T.Unicode().tag(sync=True)


@W.register
class GridStyle(W.Widget):
    """JSON-compatible Lumino `DataGrid` styles."""

    # pylint: disable=C0301
    _model_name = T.Unicode("GridStyleModel").tag(sync=True)
    _model_module = T.Unicode(module_name).tag(sync=True)
    _model_module_version = T.Unicode(module_version).tag(sync=True)

    # the part between these comments will be rewritten
    # BEGIN SCHEMAGEN:TRAITS IDataGridStyles @b911858621aef508319fec6b6d1cbe8afeeb8ffafe0646c0083d9491e3277e78
    backgroundColor = T.Unicode(
        help="""The background color for the body cells.

This color is layered on top of the `voidColor`.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    columnBackgroundColor = T.Union(
        [T.Tuple(), T.Enum([None])], allow_none=True, default_value=None
    ).tag(sync=True)
    cursorBorderColor = T.Unicode(
        help="""The border color for the cursor.""", allow_none=True, default_value=None
    ).tag(sync=True)
    cursorFillColor = T.Unicode(
        help="""The fill color for the cursor.""", allow_none=True, default_value=None
    ).tag(sync=True)
    gridLineColor = T.Unicode(
        help="""The color for the grid lines of the body cells.

The grid lines are draw on top of the cell contents.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    headerBackgroundColor = T.Unicode(
        help="""The background color for the header cells.

This color is layered on top of the `voidColor`.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    headerGridLineColor = T.Unicode(
        help="""The color for the grid lines of the header cells.

The grid lines are draw on top of the cell contents.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    headerHorizontalGridLineColor = T.Unicode(
        help="""The color for the horizontal grid lines of the header cells.

This overrides the `headerGridLineColor` option.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    headerSelectionBorderColor = T.Unicode(
        help="""The border color for a header selection.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    headerSelectionFillColor = T.Unicode(
        help="""The fill color for a header selection.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    headerVerticalGridLineColor = T.Unicode(
        help="""The color for the vertical grid lines of the header cells.

This overrides the `headerGridLineColor` option.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    horizontalGridLineColor = T.Unicode(
        help="""The color for the horizontal grid lines of the body cells.

This overrides the `gridLineColor` option.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    rowBackgroundColor = T.Union(
        [T.Tuple(), T.Enum([None])],
        help="""Realized as a functor, a single value will affect all rows, while any other value will be return modulo the position.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    scrollShadow = T.Dict(
        help="""The drop shadow effect when the grid is scrolled.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    selectionBorderColor = T.Unicode(
        help="""The border color for a selection.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    selectionFillColor = T.Unicode(
        help="""The fill color for a selection.""", allow_none=True, default_value=None
    ).tag(sync=True)
    verticalGridLineColor = T.Unicode(
        help="""The color for the vertical grid lines of the body cells.

This overrides the `gridLineColor` option.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    voidColor = T.Unicode(
        help="""The void color for the data grid.

This is the base fill color for the entire data grid.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    # END SCHEMAGEN:TRAITS


@W.register
class StyleGrid(DataGrid):
    """A styled grid

    ``[0.1.6]/datagrid.ts#L64``
    """

    # pylint: disable=no-member

    _model_name = T.Unicode("StyleGridModel").tag(sync=True)
    _view_name = T.Unicode("StyleGridView").tag(sync=True)

    row_size = T.Int().tag(sync=True)
    column_size = T.Int().tag(sync=True)
    row_header_size = T.Int().tag(sync=True)
    column_header_size = T.Int().tag(sync=True)

    header_visibility = T.Enum(
        ["all", "row", "column", "none"], default_value="all"
    ).tag(sync=True)

    grid_style = W.trait_types.InstanceDict(GridStyle).tag(
        sync=True, **W.widget_serialization
    )

    cell_renderers = T.List(T.Instance(CellRenderer)).tag(
        sync=True, **W.widget_serialization
    )
