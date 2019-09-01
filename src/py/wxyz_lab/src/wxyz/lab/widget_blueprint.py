""" Text editing widgets
"""
# pylint: disable=too-many-ancestors
from .base import LabBase, T, W


@W.register
class Icon(LabBase, W.DOMWidget):
    """ A Blueprint icon
    """

    _model_name = T.Unicode("IconModel").tag(sync=True)
    _view_name = T.Unicode("IconView").tag(sync=True)

    icon = T.Unicode().tag(sync=True)
    color = T.Unicode().tag(sync=True)
    icon_size = T.Int(16).tag(sync=True)

    def __init__(self, icon=None, **kwargs):
        kwargs["icon"] = icon
        super().__init__(**kwargs)


@W.register
class Button(LabBase, W.Button):
    """ A Blueprint button
    """

    _model_name = T.Unicode("ButtonModel").tag(sync=True)
    _view_name = T.Unicode("ButtonView").tag(sync=True)

    icon = T.Union([T.Unicode(), T.Instance(Icon)]).tag(
        sync=True, **W.widget_serialization
    )
    icon_right = T.Union([T.Unicode(), T.Instance(Icon)]).tag(
        sync=True, **W.widget_serialization
    )

    large = T.Bool(False).tag(sync=True)
    loading = T.Bool(False).tag(sync=True)
    minimal = T.Bool(False).tag(sync=True)
    small = T.Bool(False).tag(sync=True)
    active = T.Bool(False).tag(sync=True)

    @T.validate("icon")
    def _validate_icon(self, proposal):
        return proposal["value"]
