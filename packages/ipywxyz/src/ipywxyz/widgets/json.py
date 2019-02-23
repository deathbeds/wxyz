""" Widgets for working with JSON
"""
import json

from .base import Fn, T, W


@W.register
class JSON(Fn):
    """ A JSON parsing functional widget
    """

    _model_name = T.Unicode("JSONModel").tag(sync=True)

    value = T.Union([T.Dict(), T.List(), T.Unicode(), T.Int(), T.Float()]).tag(
        sync=True
    )

    @T.observe("source")
    def _source_changed(self, *_):
        self.value = json.loads(self.source)
