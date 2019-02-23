""" Widgets for working with JSON
"""
from pyld import jsonld

from .base import Fn, T, W


@W.register
class Expand(Fn):
    """ Expand a JSON document to a list of nodes
    """

    _model_name = T.Unicode("ExpandModel").tag(sync=True)

    source = T.Dict(allow_none=True).tag(sync=True)
    value = T.List(allow_none=True).tag(sync=True)
    context = T.Dict(allow_none=True).tag(sync=True)

    @T.default("source")
    @T.default("context")
    def _default_source_contex(self):
        return {}

    @T.default("value")
    def _default_value(self):
        return []

    @T.observe("source", "context")
    def _change(self, *_):
        try:
            self.error = ""
            self.value = jsonld.expand(self.source, dict(
                expandContext=self.context
            ))
        except Exception as err:
            self.error = f"{err}"


@W.register
class Compact(Fn):
    """ Compact a JSON document with a context
    """

    _model_name = T.Unicode("CompactModel").tag(sync=True)

    source = T.Dict(allow_none=True).tag(sync=True)
    value = T.Dict(allow_none=True).tag(sync=True)
    context = T.Dict(allow_none=True).tag(sync=True)
    expand_context = T.Dict(allow_none=True).tag(sync=True)

    @T.default("source")
    @T.default("context")
    @T.default("value")
    @T.default("expand_context")
    def _default(self):
        return {}

    @T.observe("source", "context", "expand_context")
    def _change(self, *_):
        try:
            self.error = ""
            self.value = jsonld.compact(self.source, self.context, dict(
                expandContext=self.expand_context
            ))
        except Exception as err:
            self.error = f"{err}"


@W.register
class Flatten(Fn):
    """ Flatten a JSON document to a flat graph
    """

    _model_name = T.Unicode("FlattenModel").tag(sync=True)

    source = T.Dict(allow_none=True).tag(sync=True)
    value = T.Dict(allow_none=True).tag(sync=True)
    context = T.Dict(allow_none=True).tag(sync=True)
    expand_context = T.Dict(allow_none=True).tag(sync=True)

    @T.default("source")
    @T.default("context")
    @T.default("value")
    @T.default("expand_context")
    def _default(self):
        return {}

    @T.observe("source", "context", "expand_context")
    def _change(self, *_):
        try:
            self.error = ""
            self.value = jsonld.flatten(self.source, self.context, dict(
                expandContext=self.expand_context
            ))
        except Exception as err:
            self.error = f"{err}"


@W.register
class Frame(Fn):
    """ Frame a JSON document
    """

    _model_name = T.Unicode("FrameModel").tag(sync=True)

    source = T.Dict(allow_none=True).tag(sync=True)
    value = T.Dict(allow_none=True).tag(sync=True)
    frame = T.Dict(allow_none=True).tag(sync=True)
    expand_context = T.Dict(allow_none=True).tag(sync=True)

    @T.default("source")
    @T.default("frame")
    @T.default("expand_context")
    @T.default("value")
    def _default(self):
        return {}

    @T.observe("source", "frame", "expand_context")
    def _change(self, *_):
        try:
            self.error = ""
            self.value = jsonld.frame(self.source, self.frame, dict(
                expandContext=self.expand_context
            ))
        except Exception as err:
            self.error = f"{err}"


@W.register
class Normalize(Fn):
    """ Normalize a JSON document
    """

    _model_name = T.Unicode("NormalizeModel").tag(sync=True)

    source = T.Dict(allow_none=True).tag(sync=True)
    value = T.Union([
        T.Dict(allow_none=True),
        T.Unicode(allow_none=True)
    ]).tag(sync=True)
    expand_context = T.Dict(allow_none=True).tag(sync=True)
    format = T.Unicode(default_value="application/n-quads",
                       allow_none=True).tag(sync=True)

    @T.default("source")
    @T.default("expand_context")
    @T.default("value")
    def _default(self):
        return {}

    @T.observe("source", "expand_context", "format")
    def _change(self, *_):
        try:
            self.error = ""
            self.value = jsonld.normalize(self.source, dict(
                expandContext=self.expand_context,
                format=self.format
            ))
        except Exception as err:
            self.error = f"{err}"
