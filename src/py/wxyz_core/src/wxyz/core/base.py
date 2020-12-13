""" Reusable boilerplate for widgets
"""
# pylint: disable=broad-except,no-member
import ipywidgets as W
import traitlets as T

from ._version import module_name, module_version


class WXYZBase(W.Widget):
    """Version and front-end metadata"""

    _model_module = T.Unicode(module_name).tag(sync=True)
    _model_module_version = T.Unicode(module_version).tag(sync=True)
    _view_module = T.Unicode(module_name).tag(sync=True)
    _view_module_version = T.Unicode(module_version).tag(sync=True)


class WXYZBox(W.Box):
    """Version and front-end metadata"""

    _model_module = T.Unicode(module_name).tag(sync=True)
    _model_module_version = T.Unicode(module_version).tag(sync=True)
    _view_module = T.Unicode(module_name).tag(sync=True)
    _view_module_version = T.Unicode(module_version).tag(sync=True)


class Base(WXYZBase):
    """Utility traitlets, primarily based around
    - development convenience
    - ipywidgets conventions
    - integration with wxyz.lab.DockBox, mostly lumino Widget.label attrs
    """

    _model_module = T.Unicode(module_name).tag(sync=True)
    _model_module_version = T.Unicode(module_version).tag(sync=True)
    _view_module = T.Unicode(module_name).tag(sync=True)
    _view_module_version = T.Unicode(module_version).tag(sync=True)

    error = T.CUnicode("").tag(sync=True)
    description = T.Unicode("An Undescribed Widget").tag(sync=True)
    icon_class = T.Unicode("jp-CircleIcon").tag(sync=True)
    closable = T.Bool(default_value=True).tag(sync=True)


class Fn(Base):
    """Turns a `source` into a `value`"""

    source = T.Any(allow_none=True).tag(sync=True)
    value = T.Any(allow_none=True).tag(sync=True)
    mode = T.Enum(["both", "kernel", "client"], default_value="both").tag(sync=True)

    _observed_traits = ["source"]

    def __init__(self, *args, **kwargs):
        for i, arg in enumerate(args):
            kwargs[self._observed_traits[i]] = arg
        super().__init__(**kwargs)
        self.observe(self.the_observer, self._observed_traits)
        self.the_observer(None)

    def the_observer(self, *_):
        """Base observer that updates value and/or error"""
        if self.mode == "client":
            return

        with self.hold_trait_notifications():
            try:
                self.value = None
                self.value = self.the_function(
                    **{t: getattr(self, t) for t in self._observed_traits}
                )
                self.error = ""
            except Exception as err:
                self.error = f"{err}"
