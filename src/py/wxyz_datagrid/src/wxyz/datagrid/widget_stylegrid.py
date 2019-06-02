""" A styled grid
"""
# pylint: disable=R0903,C0103,W0703,R0901
from wxyz.core.base import T, W, WXYZBase
from wxyz.html.widget_color import AlphaColor, EmptyAlphaColor

from .base import DataGridBase
from .widget_datagrid import DataGrid


@W.register
class CellRenderer(WXYZBase, DataGridBase):
    """ [0.1.6]/cellrenderer.ts#L29
    """

    _model_name = T.Unicode("CellRendererModel").tag(sync=True)

    region = T.Unicode("body").tag(sync=True)
    metadata = T.Dict().tag(sync=True)


@W.register
class FormatFunc(WXYZBase, DataGridBase):
    """ [0.1.6]/textrenderer.ts#L308
    """

    _model_name = T.Unicode("FormatFuncModel").tag(sync=True)


@W.register
class TextRenderer(CellRenderer, DataGridBase):
    """ [0.1.6]/textrenderer.ts#L21
    """

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
    """ [0.1.6]/textrenderer.ts#L365
    """

    _model_name = T.Unicode("FixedFuncModel").tag(sync=True)

    digits = T.Int().tag(sync=True)
    missing = T.Unicode().tag(sync=True)


@W.register
class StyleGrid(DataGrid):
    """ A styled grid
        [0.1.6]/datagrid.ts#L64
    """

    _model_name = T.Unicode("StyleGridModel").tag(sync=True)
    _view_name = T.Unicode("StyleGridView").tag(sync=True)

    row_size = T.Int().tag(sync=True)
    column_size = T.Int().tag(sync=True)
    row_header_size = T.Int().tag(sync=True)
    column_header_size = T.Int().tag(sync=True)

    void_color = AlphaColor("#F3F3F3").tag(sync=True)
    background_color = AlphaColor("#FFFFFF").tag(sync=True)
    grid_line_color = AlphaColor("rgba(20, 20, 20, 0.15)").tag(sync=True)
    header_background_color = AlphaColor("#F3F3F3").tag(sync=True)
    header_grid_line_color = AlphaColor("rgba(20, 20, 20, 0.25)").tag(sync=True)

    cell_renderers = T.List(T.Instance(CellRenderer)).tag(
        sync=True, **W.widget_serialization
    )
