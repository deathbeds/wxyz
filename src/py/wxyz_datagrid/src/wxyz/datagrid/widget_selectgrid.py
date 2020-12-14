""" A selectable Data Frame
"""
# pylint: disable=R0903,C0103,W0703,R0901

from .base import TT, T, W
from .widget_stylegrid import StyleGrid


@W.register
class SelectGrid(StyleGrid):
    """A styled grid with selections"""

    _model_name = T.Unicode("SelectGridModel").tag(sync=True)
    _view_name = T.Unicode("SelectGridView").tag(sync=True)

    scroll_x = T.Int(0).tag(sync=True)
    scroll_y = T.Int(0).tag(sync=True)

    max_x = T.Int(100).tag(sync=True)
    max_y = T.Int(100).tag(sync=True)

    hover_row = T.Int(0).tag(sync=True)
    hover_column = T.Int(0).tag(sync=True)

    viewport = T.Tuple(
        T.Int(),
        T.Int(),
        T.Int(),
        T.Int(),
        default_value=[0, 0, 0, 0],
        help="the current viewport as [c0, c1, r0, r1]",
    ).tag(sync=True)

    selections = TT.TypedTuple(
        T.Tuple(T.Int(), T.Int(), T.Int(), T.Int(), default_value=[0, 0, 0, 0]),
        help="all current selections as [c0, c1, r0, r1]",
    ).tag(sync=True)

    selection = T.Tuple(
        T.Int(),
        T.Int(),
        T.Int(),
        T.Int(),
        default_value=[0, 0, 0, 0],
        help="the first selection as [c0, c1, r0, r1]",
    ).tag(sync=True)
