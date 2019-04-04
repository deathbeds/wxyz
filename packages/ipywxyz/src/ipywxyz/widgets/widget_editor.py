""" Text editing widgets
"""
# pylint: disable=too-many-ancestors
from ._base import Base, T, W
from . import abbrev


@W.register
class Editor(Base, W.Textarea, W.ValueWidget):
    """ A basic editor
    """

    _model_name = T.Unicode("EditorModel").tag(sync=True)
    _view_name = T.Unicode("EditorView").tag(sync=True)


abbrev.for_type(str, lambda x: Editor(value=x, **abbrev.BLOCK_LAYOUT))
