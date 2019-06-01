""" Full Screen widget
"""
# pylint: disable=too-many-ancestors
from wxyz.core.base import Base, T, W


@W.register
class Fullscreen(Base, W.Box):
    """ A full screen container
    """

    _model_name = T.Unicode("FullscreenModel").tag(sync=True)
    _view_name = T.Unicode("FullscreenView").tag(sync=True)
