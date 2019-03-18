""" Some widgets
"""
# flake8: noqa
from ._version import __version__, version_info

# these just emulate stuff in lab
from .widgets.widget_dock import DockBox, DockPop
from .widgets.widget_editor import Editor

# some of these have dependencies that might fail
try:
    from .widgets.widget_json import JSON, JSONPointer, JSONSchema
except ImportError:
    pass

try:
    from .widgets.widget_jsonld import Expand, Compact, Flatten, Frame, Normalize
except ImportError:
    pass

try:
    from .widgets.widget_markdown import Markdown
except ImportError:
    pass

try:
    from .widgets.widget_template import Template
except ImportError:
    pass
