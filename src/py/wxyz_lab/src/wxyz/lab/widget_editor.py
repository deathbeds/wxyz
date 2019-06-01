""" Text editing widgets
"""
# pylint: disable=too-many-ancestors
from wxyz.core.base import Base, T, W


@W.register
class Editor(Base, W.Textarea):
    """ A basic editor
    """

    _model_name = T.Unicode("EditorModel").tag(sync=True)
    _view_name = T.Unicode("EditorView").tag(sync=True)
