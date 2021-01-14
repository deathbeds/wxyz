""" Full Screen widget
"""
from .base import HTMLBase, T, W


@W.register
class Fullscreen(HTMLBase, W.Box):
    """A full-screen Box, activated with Ctrl+Shift+Click, or the flower key on MacOS"""

    _model_name = T.Unicode("FullscreenModel").tag(sync=True)
    _view_name = T.Unicode("FullscreenView").tag(sync=True)
