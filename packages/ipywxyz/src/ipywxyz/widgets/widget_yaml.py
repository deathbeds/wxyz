""" Widgets for working with YAML
"""
# pylint: disable=too-many-ancestors,no-self-use
from yaml import safe_load

from ._base import T, W
from .widget_json import JSON


@W.register
class YAML(JSON):
    """ A Widget that parses YAML source into... something
    """

    _model_name = T.Unicode("YAMLModel").tag(sync=True)

    def the_function(self, source):
        """ "safely" load some YAML
        """
        return safe_load(source)
