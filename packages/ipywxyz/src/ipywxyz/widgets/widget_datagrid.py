""" A datagrid
"""
import json
import re

import pandas as pd
import traittypes as TT

from ._base import Base, T, W

TABLE = {"orient": "table"}

dataframe_serialization = dict(
    to_json=lambda df, obj: None if df is None else df.to_dict(orient="table"),
    from_json=lambda value, obj: None if value is None else pd.DataFrame(value),
)
_rgb_eh = re.compile(r"rgba?\(\d+,\s*\d+,\s*\d+,\s*[10](\.\d+)?\)")


class MoreColor(W.trait_types.Color):
    def validate(self, obj, value):
        if _rgb_eh.match(value):
            return value
        return super(MoreColor, self).validate(obj, value)


class MoreColorPicker(W.ColorPicker):
    value = MoreColor("rgba(128, 128, 128, 0.5)").tag(sync=True)


@W.register
class DataGrid(Base, W.Box):
    value = TT.DataFrame(None, allow_none=True).tag(
        sync=True,
        to_json=lambda df, obj: None if df is None else json.loads(df.to_json(**TABLE)),
        from_json=lambda value, obj: None
        if value is None
        else pd.read_json(json.dumps(value), **TABLE),
    )
    x = T.Int().tag(sync=True)
    y = T.Int().tag(sync=True)
    max_x = T.Int().tag(sync=True)
    max_y = T.Int().tag(sync=True)
    row_size = T.Int().tag(sync=True)
    column_size = T.Int().tag(sync=True)
    row_header_size = T.Int().tag(sync=True)
    column_header_size = T.Int().tag(sync=True)
    void_color = MoreColor("#F3F3F3").tag(sync=True)
    background_color = MoreColor("#FFFFFF").tag(sync=True)
    grid_line_color = MoreColor("rgba(20, 20, 20, 0.15)").tag(sync=True)
    header_background_color = MoreColor("#F3F3F3").tag(sync=True)
    header_grid_line_color = MoreColor("rgba(20, 20, 20, 0.25)").tag(sync=True)

    _model_name = T.Unicode("DataGridModel").tag(sync=True)
    _view_name = T.Unicode("DataGridView").tag(sync=True)

    def _repr_keys(self):
        try:
            super_keys = super(DataGrid, self)._repr_keys()
            for key in super_keys:
                if key != "value":
                    yield key
        except Exception:
            return
