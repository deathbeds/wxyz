""" Text editing widgets
"""
from .base import LabBase, T, W, module_name, module_version


@W.register
class EditorConfig(W.Widget):
    """CodeMirror-compatible options.

    TODO: generate schema from typings, and then this class
    """

    _model_name = T.Unicode("EditorConfigModel").tag(sync=True)
    _model_module = T.Unicode(module_name).tag(sync=True)
    _model_module_version = T.Unicode(module_version).tag(sync=True)

    mode = T.Unicode().tag(sync=True)
    theme = T.Unicode().tag(sync=True)


@W.register
class Editor(LabBase, W.Textarea):
    """A basic editor"""

    # pylint: disable=no-member

    value = T.Any().tag(sync=True)

    _model_name = T.Unicode("EditorModel").tag(sync=True)
    _view_name = T.Unicode("EditorView").tag(sync=True)

    config = W.trait_types.InstanceDict(EditorConfig).tag(
        sync=True, **W.widget_serialization
    )
