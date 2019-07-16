""" Widgets for working with YAML
"""
# pylint: disable=too-many-ancestors,no-self-use,too-few-public-methods
from yaml import safe_load

from wxyz.core.widget_json import JSON

from .base import T, W, CytoscapeBase


@W.register
class Cytoscape(CytoscapeBase):
    """ A Widget that renders Cytoscape JSON
    """
    value = T.Dict().tag(sync=True)
    layout = T.Unicode(allow_none=True).tag(sync=True)

    _model_name = T.Unicode("CytoscapeModel").tag(sync=True)
    _view_name = T.Unicode("CytoscapeView").tag(sync=True)

    @T.default("value")
    def _default_value():
        return {
            "elements": {
                "nodes": [],
                "edges": []
            },
            "data": {
                "name": "Untitled Graph"
            }
        }
