""" Reusable boilerplate for widgets
"""
# pylint: disable=broad-except,no-member,too-few-public-methods

import ipywidgets as W
import traitlets as T

from ._version import module_name, module_version


class WXYZ_MODE:
    """locations of WXYZ execution

    Should probably be an enum.
    """

    kernel = "kernel"
    client = "client"
    both = "both"


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

    error = T.CUnicode("").tag(sync=True)  # type: str
    description = T.Unicode("An Undescribed Widget").tag(sync=True)  # type: str
    icon_class = T.Unicode("jp-CircleIcon").tag(sync=True)  # type: str
    closable = T.Bool(default_value=True).tag(sync=True)  # type: bool


class Fn(Base):
    """Turns a ``source`` into a ``value``

    This is a foundational class with a number of implementations throughout
    ``wxyz``.

    The simplest ``Fn`` subclass might implement the *identity function*:

    .. code-block:: python

        class Identity(Fn):
            def the_function(self, source):
                return source

    .. note:

        On the TypeScript side, the identity function might look like:

        .. code-block: typescript

            async theFunction(source: T): Promise<U> {
              return source as U;
            }

    """

    #: the source
    source = T.Any(allow_none=True).tag(sync=True)  # type: any

    #: the value produced by evaluating the function
    value = T.Any(allow_none=True).tag(sync=True)  # type: any

    #: whether to execute transformations on the client and/or the kernel
    mode = T.Enum(
        [WXYZ_MODE.both, WXYZ_MODE.client, WXYZ_MODE.kernel],
        default_value=WXYZ_MODE.both,
    ).tag(sync=True)

    # these are the function inputs, beyond the source
    _observed_traits = ["source"]

    def __init__(self, *args, **kwargs):
        for i, arg in enumerate(args):
            kwargs[self._observed_traits[i]] = arg
        super().__init__(**kwargs)
        self.observe(self.the_observer, self._observed_traits)
        self.the_observer(None)

    def the_observer(self, *_):
        """Base observer that updates value and/or error"""
        if self.mode == WXYZ_MODE.client:
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
