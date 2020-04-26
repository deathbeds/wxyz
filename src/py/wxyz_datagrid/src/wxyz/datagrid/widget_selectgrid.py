""" A selectable Data Frame
"""
# pylint: disable=R0903,C0103,W0703,R0901
from wxyz.html import AlphaColor

from .base import T, W
from .widget_stylegrid import StyleGrid


@W.register
class SelectGrid(StyleGrid):
    """ A styled grid with selections
    """

    _model_name = T.Unicode("SelectGridModel").tag(sync=True)
    _view_name = T.Unicode("SelectGridView").tag(sync=True)

    scroll_x = T.Int(0).tag(sync=True)
    scroll_y = T.Int(0).tag(sync=True)

    max_x = T.Int(100).tag(sync=True)
    max_y = T.Int(100).tag(sync=True)

    hover_row = T.Int(0).tag(sync=True)
    hover_column = T.Int(0).tag(sync=True)

    viewport = T.Tuple(
        T.Int(), T.Int(), T.Int(), T.Int(), default_value=[0, 0, 0, 0]
    ).tag(sync=True)

    selection = T.Tuple(
        T.Int(), T.Int(), T.Int(), T.Int(), default_value=[0, 0, 0, 0]
    ).tag(sync=True)
    selecting = T.Bool(False).tag(sync=True)
    selection_color = AlphaColor("rgba(0,0,255,0.125)").tag(sync=True)
