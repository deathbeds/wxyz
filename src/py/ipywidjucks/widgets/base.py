import ipywidgets as W
import traitlets as T
from .._version import module_name, module_version


class Base(W.Widget):
    _model_module = T.Unicode(module_name).tag(sync=True)
    _model_module_version = T.Unicode(module_version).tag(sync=True)

    error = T.Unicode().tag(sync=True)
