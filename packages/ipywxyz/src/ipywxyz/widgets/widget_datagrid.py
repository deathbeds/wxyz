""" A datagrid
"""
# pylint: disable=R0903,C0103,W0703,R0901
import json

import pandas as pd
import traittypes as TT

from ._base import Base, T, W
from .widget_color import AlphaColor

TABLE = {"orient": "table"}

dataframe_serialization = dict(
    to_json=lambda df, obj: None if df is None else df.to_dict(orient="table"),
    from_json=lambda value, obj: None if value is None else pd.DataFrame(value),
)


@W.register
class DataGrid(Base, W.Box):
    """ An (overly) opinionated DataFrame-backed datagrid
    """

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

    _model_name = T.Unicode("DataGridModel").tag(sync=True)
    _view_name = T.Unicode("DataGridView").tag(sync=True)

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
