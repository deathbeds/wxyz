""" A selectable Data Frame
"""
# pylint: disable=R0903,C0103,W0703,R0901
from . import abbrev
from ._base import T, W
from .widget_color import AlphaColor
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

    _observed = False

    def get_interact_value(self):
        if not self._observed:
            def on_change(change):
                self._notify_trait("value", self.value, self.value)
            self.observe(on_change, 'selection')
            self._observed = True
        s = self.selection
        return self.value.iloc[s[2]: s[3]+ 1, s[0]:s[1] + 1]


abbrev.for_type_by_name(
    'pandas.core.frame',
    'DataFrame',
    lambda x: SelectGrid(value=x, **abbrev.BLOCK_LAYOUT)
)
