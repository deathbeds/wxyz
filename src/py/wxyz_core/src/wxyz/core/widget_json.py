""" Widgets for working with JSON
"""
# pylint: disable=no-self-use
import json

import jsonpointer
import jsonschema

from .base import Fn, T, W


@W.register
class JSON(Fn):
    """A JSON parsing functional widget"""

    _model_name = T.Unicode("JSONModel").tag(sync=True)

    value = T.Union(
        [T.Dict(), T.List(), T.Unicode(), T.Int(), T.Float(), T.Bool()], allow_none=True
    ).tag(sync=True)

    def the_function(self, source):
        """parse some JSON"""
        return json.loads(source)


@W.register
class UnJSON(Fn):
    """A JSON dumping functional widget"""

    _model_name = T.Unicode("UnJSONModel").tag(sync=True)

    source = T.Union(
        [T.Dict(), T.List(), T.Unicode(), T.Int(), T.Float(), T.Bool()], allow_none=True
    ).tag(sync=True)
    value = T.Unicode(allow_none=True).tag(sync=True)
    indent = T.Int(allow_none=True).tag(sync=True)

    _observed_traits = ["source", "indent"]

    def the_function(self, source, indent):
        """dump some JSON"""
        kwargs = {}
        if indent:
            kwargs["indent"] = indent
        return json.dumps(source, **kwargs)


@W.register
class JSONPointer(Fn):
    """A JSON pointer resolver"""

    _model_name = T.Unicode("JSONPointerModel").tag(sync=True)

    source = T.Dict(allow_none=True).tag(sync=True)
    pointer = T.Unicode(allow_none=True).tag(sync=True)

    _observed_traits = ["source", "pointer"]

    def the_function(self, source, pointer):
        """point at some json"""
        return jsonpointer.resolve_pointer(source, pointer)


@W.register
class JSONSchema(Fn):
    """A JSON schema validator"""

    _model_name = T.Unicode("JSONSchemaModel").tag(sync=True)

    source = T.Dict(allow_none=True).tag(sync=True)
    schema = T.Dict(allow_none=True).tag(sync=True)
    value = T.Dict(allow_none=True).tag(sync=True)

    _observed_traits = ["source", "schema"]

    def the_function(self, source, schema):
        """validate some JSON"""
        jsonschema.validate(source, schema)
        return source
