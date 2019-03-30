""" A selectable Data Frame
"""
# pylint: disable=R0903,C0103,W0703,R0901
from ._base import T, W
from .widget_stylegrid import StyleGrid


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

    selection = T.Tuple(
        T.Int(), T.Int(), T.Int(), T.Int(), default_value=[0, 0, 0, 0]
    ).tag(sync=True)
    selecting = T.Bool().tag(sync=True)
