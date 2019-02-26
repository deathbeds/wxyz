""" Some widgets
"""
# flake8: noqa
from ._version import __version__
from ._version import version_info
from .widgets.widget_dock import DockBox
from .widgets.widget_editor import Editor
from .widgets.widget_json import JSON, JSONPointer, JSONSchema
from .widgets.widget_jsonld import Expand, Compact, Flatten, Frame, Normalize
from .widgets.widget_markdown import Markdown
from .widgets.widget_template import Template


def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static/wxyz',
        'dest': 'wxyz-nbextension',
        'require': 'wxyz-nbextension/index'
    }]
