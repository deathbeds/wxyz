""" Reusable boilerplate for widgets
"""
import ipywidgets as W
import traitlets as T

from .._version import module_name, module_version


class Base(W.Widget):
    """ A widget hoping to go places
    """

    _model_module = T.Unicode(module_name).tag(sync=True)
    _model_module_version = T.Unicode(module_version).tag(sync=True)
    _view_module = T.Unicode(module_name).tag(sync=True)
    _view_module_version = T.Unicode(module_version).tag(sync=True)

    error = T.Unicode("").tag(sync=True)
    description = T.Unicode("An Undescribed Widget").tag(sync=True)
    icon_class = T.Unicode("jp-CircleIcon").tag(sync=True)
    closable = T.Bool(default_value=True).tag(sync=True)


class Fn(Base):
    """ A widget that turns a source into a value
    """

    source = T.Unicode("").tag(sync=True)
    value = T.Unicode("").tag(sync=True)

    def __init__(self, source="", **kwargs):
        super(Fn, self).__init__(source=source, **kwargs)
