""" Widgets that render in the dock
"""
# pylint: disable=too-many-ancestors
from ._base import Base, T, W


@W.register
class DockBox(Base, W.Box):
    """ A Box that renders as a DockPanel
    """

    _model_name = T.Unicode("DockBoxModel").tag(sync=True)
    _view_name = T.Unicode("DockBoxView").tag(sync=True)
