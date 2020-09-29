""" Widgets for working with JSON
"""
# pylint: disable=no-self-use,redefined-builtin
from pyld import jsonld

from wxyz.core.base import Fn, T, W

from .base import JSONLDBase


@W.register
class Compact(Fn, JSONLDBase):
    """Compact a JSON document with a context"""

    _model_name = T.Unicode("CompactModel").tag(sync=True)

    source = T.Dict(allow_none=True).tag(sync=True)
    context = T.Dict(allow_none=True).tag(sync=True)
    expand_context = T.Dict(allow_none=True).tag(sync=True)

    value = T.Dict(allow_none=True).tag(sync=True)

    _observed_traits = ["source", "context", "expand_context"]

    def the_function(self, source, context, expand_context):
        """actually compact"""
        return jsonld.compact(source, context, dict(expandContext=expand_context))


@W.register
class Expand(Fn, JSONLDBase):
    """Expand a JSON document to a list of nodes"""

    _model_name = T.Unicode("ExpandModel").tag(sync=True)

    source = T.Dict(allow_none=True).tag(sync=True)
    expand_context = T.Dict(allow_none=True).tag(sync=True)
    value = T.List(allow_none=True).tag(sync=True)

    _observed_traits = ["source", "expand_context"]

    def the_function(self, source, expand_context):
        """actually expand"""
        return jsonld.expand(source, dict(expandContext=expand_context))


@W.register
class Flatten(Fn, JSONLDBase):
    """Flatten a JSON document to a flat graph"""

    _model_name = T.Unicode("FlattenModel").tag(sync=True)

    source = T.Dict(allow_none=True).tag(sync=True)
    context = T.Dict(allow_none=True).tag(sync=True)
    expand_context = T.Dict(allow_none=True).tag(sync=True)

    value = T.Dict(allow_none=True).tag(sync=True)

    _observed_traits = ["source", "context", "expand_context"]

    def the_function(self, source, context, expand_context):
        """actually flatten"""
        return jsonld.flatten(source, context, dict(expandContext=expand_context))


@W.register
class Frame(Fn, JSONLDBase):
    """Frame a JSON document"""

    _model_name = T.Unicode("FrameModel").tag(sync=True)

    source = T.Dict(allow_none=True).tag(sync=True)
    frame = T.Dict(allow_none=True).tag(sync=True)
    expand_context = T.Dict(allow_none=True).tag(sync=True)

    value = T.Dict(allow_none=True).tag(sync=True)

    _observed_traits = ["source", "frame", "expand_context"]

    def the_function(self, source, frame, expand_context):
        """actually frame"""
        return jsonld.frame(source, frame, dict(expandContext=expand_context))


@W.register
class Normalize(Fn, JSONLDBase):
    """Normalize a JSON document"""

    _model_name = T.Unicode("NormalizeModel").tag(sync=True)

    _observed_traits = ["source", "frame", "expand_context"]

    source = T.Dict(allow_none=True).tag(sync=True)
    expand_context = T.Dict(allow_none=True).tag(sync=True)
    format = T.Unicode(default_value="application/n-quads", allow_none=True).tag(
        sync=True
    )

    value = T.Union([T.Dict(allow_none=True), T.Unicode(allow_none=True)]).tag(
        sync=True
    )

    _observed_traits = ["source", "format", "expand_context"]

    def the_function(self, source, format, expand_context):
        """actually normalize"""
        return jsonld.normalize(
            source, dict(expandContext=expand_context, format=format)
        )
