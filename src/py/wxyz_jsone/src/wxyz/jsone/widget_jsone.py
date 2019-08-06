""" Widgets for working with JSON
"""
# pylint: disable=no-self-use,redefined-builtin,too-many-ancestors
import jsone

from wxyz.core.base import Fn, T, W

from .base import JSONEBase


@W.register
class JSONE(Fn, JSONEBase):
    """ Transform a JSON document
    """

    _model_name = T.Unicode("JSONEModel").tag(sync=True)

    source = T.Any(allow_none=True).tag(sync=True)
    context = T.Any(allow_none=True).tag(sync=True)
    value = T.Any(allow_none=True).tag(sync=True)

    _observed_traits = ["source", "context"]

    def the_function(self, source, context):
        """ actually compact
        """
        return jsone.render(source, context)
