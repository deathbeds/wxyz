""" Widgets to (sometimes) efficiently model data sources
"""
import json

import ipydatawidgets as D

# pylint: disable=too-many-ancestors,broad-except
import numpy as np
import pandas as pd
import traittypes as TT

from ._base import T, W, WXYZBase

TABLE = {"orient": "table"}


@W.register
class DataSource(WXYZBase):
    """ A WXYZ data source
    """

    _model_name = T.Unicode("DataSourceModel").tag(sync=True)


@W.register
class TableSchemaSource(DataSource):
    """ A DataGrid-compatible source for a pandas DataFrame (or any JSON Table
        Schema compatible source, PRs welcome!)

        Tables bigger than 1000 on a side can get slow to load (but will remain)
        smooth once loaded.
    """

    _model_name = T.Unicode("TableSchemaSourceModel").tag(sync=True)
    value = TT.DataFrame(None, allow_none=True).tag(
        sync=True,
        to_json=lambda df, obj: None if df is None else json.loads(df.to_json(**TABLE)),
        from_json=lambda value, obj: None
        if value is None
        else pd.read_json(json.dumps(value), **TABLE),
    )

    def _repr_keys(self):
        """ this shouldn't be needed, but we're doing _something wrong_
        """
        try:
            super_keys = super(TableSchemaSource, self)._repr_keys()
            for key in super_keys:
                if key != "value":
                    yield key
        except Exception:
            return


@W.register
class NDArraySource(DataSource):
    """ A GridPanel-compatible source of a single data type
    """

    _model_name = T.Unicode("NDArraySourceModel").tag(sync=True)
    value = D.DataUnion(np.zeros(0)).tag(sync=True)


@W.register
class ColumnarSource(DataSource):
    """ A GridPanel-compatible source of typed columns
    """

    _model_name = T.Unicode("ColumnarSourceModel").tag(sync=True)
    value = T.List(D.DataUnion(np.zeros(0))).tag(sync=True, **W.widget_serialization)
