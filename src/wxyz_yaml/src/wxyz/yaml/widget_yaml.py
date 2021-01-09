""" Widgets for working with YAML
"""
# pylint: disable=no-self-use,too-few-public-methods
# pylint: disable=no-name-in-module,cyclic-import
from yaml import safe_dump, safe_load

from wxyz.core import JSON, UnJSON

from .base import T, W, YAMLBase


@W.register
class YAML(JSON, YAMLBase):
    """A Widget that parses YAML source into... something"""

    _model_name = T.Unicode("YAMLModel").tag(sync=True)

    def the_function(self, source):
        """ "safely" load some YAML"""
        return safe_load(source)


@W.register
class UnYAML(UnJSON, YAMLBase):
    """A Widget that dumps... something into YAML"""

    _model_name = T.Unicode("UnYAMLModel").tag(sync=True)

    def the_function(self, source, indent):
        """ "safely" dump some YAML"""
        return safe_dump(source, indent=indent, default_flow_style=False)
