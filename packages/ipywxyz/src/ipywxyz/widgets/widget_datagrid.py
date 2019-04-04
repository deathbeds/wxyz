""" Jupyter Widgets for `@phosphor/datagrid`
[0.1.6]: https://github.com/phosphorjs/phosphor/blob/cdb412e9dfb/packages/datagrid/src

Notes:
- a future implementation would split the grid from the data source
"""
# pylint: disable=R0903,C0103,W0703,R0901
from ._base import Base, T, W
from .widget_datasource import WXYZDataSource

TABLE = {"orient": "table"}


@W.register
class DataGrid(Base, W.Box):
    """ An (overly) opinionated DataFrame-backed datagrid
        [0.1.6]/datagrid.ts#L64

        Used JSONModel, which expect JSON Table Schema
        [0.1.6]/jsonmodel.ts#L21
    """

    _model_name = T.Unicode("DataGridModel").tag(sync=True)
    _view_name = T.Unicode("DataGridView").tag(sync=True)

    source = T.Instance(WXYZDataSource, allow_none=True).tag(
        sync=True, **W.widget_serialization
    )
