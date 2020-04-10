""" Text editing widgets
"""
# pylint: disable=too-many-ancestors
from .base import LabBase, T, W


@W.register
class Editor(LabBase, W.Textarea):
    """ A basic editor
    """

    value = T.Any().tag(sync=True)

    _model_name = T.Unicode("EditorModel").tag(sync=True)
    _view_name = T.Unicode("EditorView").tag(sync=True)
