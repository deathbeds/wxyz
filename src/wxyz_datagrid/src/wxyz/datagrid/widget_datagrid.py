""" Jupyter Widgets for `@lumino/datagrid`
[0.6.0]: https://github.com/jupyterlab/lumino/tree/master/packages/datagrid

Notes:
- a future implementation would split the grid from the data source
"""
# pylint: disable=R0903,C0103,W0703,R0901
import json

import pandas as pd
import traittypes as TT

from .base import DataGridBase, T, W

TABLE = {"orient": "table"}

dataframe_serialization = dict(
    to_json=lambda df, obj: None if df is None else df.to_dict(orient="table"),
    from_json=lambda value, obj: None if value is None else pd.DataFrame(value),
)


@W.register
class DataGrid(DataGridBase, W.Box):
    """An (overly) opinionated `DataFrame`-backed datagrid
    ``[0.1.6]/datagrid.ts#L64``

    Used JSONModel, which expect JSON Table Schema
    ``[0.1.6]/jsonmodel.ts#L21``
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

    def _repr_keys(self):
        """this shouldn't be needed, but we're doing _something wrong_"""
        try:
            super_keys = super()._repr_keys()
            for key in super_keys:
                if key != "value":
                    yield key
        except Exception:
            return
