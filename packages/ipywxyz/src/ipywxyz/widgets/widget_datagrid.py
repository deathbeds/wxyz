""" Jupyter Widgets for `@phosphor/datagrid`
[0.1.6]: https://github.com/phosphorjs/phosphor/blob/cdb412e9dfb/packages/datagrid/src

Notes:
- a future implementation would split the grid from the data source
"""
# pylint: disable=R0903,C0103,W0703,R0901
import json

import pandas as pd
import traittypes as TT

from ._base import Base, T, W, WXYZBase
from .widget_color import AlphaColor, EmptyAlphaColor

TABLE = {"orient": "table"}

dataframe_serialization = dict(
    to_json=lambda df, obj: None if df is None else df.to_dict(orient="table"),
    from_json=lambda value, obj: None if value is None else pd.DataFrame(value),
)


class CellRenderer(WXYZBase):
    """ [0.1.6]/cellrenderer.ts#L29
    """

    _model_name = T.Unicode("CellRendererModel").tag(sync=True)

    region = T.Unicode("body").tag(sync=True)
    metadata = T.Dict().tag(sync=True)


class FormatFunc(WXYZBase):
    """ [0.1.6]/textrenderer.ts#L308
    """

    _model_name = T.Unicode("FormatFuncModel").tag(sync=True)


class TextRenderer(CellRenderer):
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


class FixedFunc(FormatFunc):
    """ [0.1.6]/textrenderer.ts#L365
    """

    _model_name = T.Unicode("FixedFuncModel").tag(sync=True)

    digits = T.Int().tag(sync=True)
    missing = T.Unicode().tag(sync=True)


@W.register
class DataGrid(Base, W.Box):
    """ An (overly) opinionated DataFrame-backed datagrid
        [0.1.6]/datagrid.ts#L64

        Used JSONModel, which expect JSON Table Schema
        [0.1.6]/jsonmodel.ts#L21
    """

    _model_name = T.Unicode("DataGridModel").tag(sync=True)
    _view_name = T.Unicode("DataGridView").tag(sync=True)

    value = TT.DataFrame(None, allow_none=True).tag(
        sync=True,
        to_json=lambda df, obj: None if df is None else json.loads(df.to_json(**TABLE)),
        from_json=lambda value, obj: None
        if value is None
        else pd.read_json(json.dumps(value), **TABLE),
    )
    scroll_x = T.Int().tag(sync=True)
    scroll_y = T.Int().tag(sync=True)
    max_x = T.Int().tag(sync=True)
    max_y = T.Int().tag(sync=True)

    row_size = T.Int().tag(sync=True)
    column_size = T.Int().tag(sync=True)
    row_header_size = T.Int().tag(sync=True)
    column_header_size = T.Int().tag(sync=True)

    void_color = AlphaColor("#F3F3F3").tag(sync=True)
    background_color = AlphaColor("#FFFFFF").tag(sync=True)
    grid_line_color = AlphaColor("rgba(20, 20, 20, 0.15)").tag(sync=True)
    header_background_color = AlphaColor("#F3F3F3").tag(sync=True)
    header_grid_line_color = AlphaColor("rgba(20, 20, 20, 0.25)").tag(sync=True)

    hover_row = T.Int().tag(sync=True)
    hover_column = T.Int().tag(sync=True)

    cell_renderers = T.List(T.Instance(CellRenderer)).tag(
        sync=True, **W.widget_serialization
    )

    def _repr_keys(self):
        """ this shouldn't be needed, but we're doing _something wrong_
        """
        try:
            super_keys = super(DataGrid, self)._repr_keys()
            for key in super_keys:
                if key != "value":
                    yield key
        except Exception:
            return
