""" Widgets for working with YAML
"""
# pylint: disable=too-many-ancestors
from yaml import safe_load

from .base import T, W
from .json import JSON


@W.register
class YAML(JSON):
    """ A Widget that parses YAML source into... something
    """

    _model_name = T.Unicode("YAMLModel").tag(sync=True)

    @T.observe("source")
    def _source_changed(self, *_):
        self.value = safe_load(self.source)
