""" Widgets for working with YAML
"""
# pylint: disable=too-many-ancestors,no-self-use,too-few-public-methods
from yaml import safe_load

from wxyz.core.base import T, W
from wxyz.core.widget_json import JSON


@W.register
class YAML(JSON):
    """ A Widget that parses YAML source into... something
    """

    _model_name = T.Unicode("YAMLModel").tag(sync=True)

    def the_function(self, source):
        """ "safely" load some YAML
        """
        return safe_load(source)
