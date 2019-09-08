""" JSS Box widget
"""
# pylint: disable=too-many-ancestors,unused-argument
from .base import JSSBase, T, W


@W.register
class JSS(JSSBase, W.Box):
    """ An JSS stylesheet which can be linked to widgets
    """

    _model_name = T.Unicode("JSSModel").tag(sync=True)
    _view_name = T.Unicode("JSSView").tag(sync=True)

    jss = T.Dict(help="a JSS object").tag(sync=True)
    widgets = T.Dict(help="a map of class names to widgets").tag(
        sync=True, **W.widget_serialization
    )
