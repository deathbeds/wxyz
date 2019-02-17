import ipywidgets as W
import traitlets as T
from ._frontend import module_name, module_version

class WidjuckBase(W.DOMWidget):
    _model_name = T.Unicode('WidjuckModel').tag(sync=True)
    _model_module = T.Unicode(module_name).tag(sync=True)
    _model_module_version = T.Unicode(module_version).tag(sync=True)
    _view_name = T.Unicode('WidjuckView').tag(sync=True)
    _view_module = T.Unicode(module_name).tag(sync=True)
    _view_module_version = T.Unicode(module_version).tag(sync=True)

class Widjuck(WidjuckBase):
    value = T.Unicode('').tag(sync=True)
    template = T.Unicode('').tag(sync=True)
    template_context = T.Dict().tag(sync=True)

    @T.default("template_context")
    def default_template_context(self):
        return {}
