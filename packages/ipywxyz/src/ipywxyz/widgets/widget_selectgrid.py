""" A selectable Data Frame
"""
# pylint: disable=R0903,C0103,W0703,R0901
import bqplot.scales as BQS

from ._base import T, W, WXYZBase
from .widget_color import EmptyAlphaColor
from .widget_stylegrid import StyleGrid


@W.register
class GridSelection(WXYZBase):
    """ The bounds of a selection of a grid
    """

    _model_name = T.Unicode("GridSelectionModel").tag(sync=True)
    _view_name = T.Unicode("GridSelectionView").tag(sync=True)

    scales = T.Dict(trait=T.List(trait=T.Instance(BQS.Scale))).tag(
        sync=True, **W.widget_serialization
    )
    color = EmptyAlphaColor().tag(sync=True)


@W.register
class SelectGrid(StyleGrid):
    """ A styled grid with selections
    """

    _model_name = T.Unicode("SelectGridModel").tag(sync=True)
    _view_name = T.Unicode("SelectGridView").tag(sync=True)

    scroll_x = T.Int().tag(sync=True)
    scroll_y = T.Int().tag(sync=True)

    max_x = T.Int().tag(sync=True)
    max_y = T.Int().tag(sync=True)

    hover_row = T.Int().tag(sync=True)
    hover_column = T.Int().tag(sync=True)

    selection = T.Instance(GridSelection).tag(sync=True, **W.widget_serialization)
