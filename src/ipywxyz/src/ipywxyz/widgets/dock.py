from .base import Base, T, W


@W.register
class DockBox(Base, W.Box):
    _model_name = T.Unicode("DockBoxModel").tag(sync=True)
    _view_name = T.Unicode("DockBoxView").tag(sync=True)
