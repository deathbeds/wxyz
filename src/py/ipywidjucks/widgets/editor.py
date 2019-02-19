from .base import Base
from .base import T
from .base import W


@W.register
class Editor(Base, W.Textarea):
    _model_name = T.Unicode("EditorModel").tag(sync=True)
    _view_name = T.Unicode("EditorView").tag(sync=True)

    mode = T.Unicode("").tag(sync=True)
