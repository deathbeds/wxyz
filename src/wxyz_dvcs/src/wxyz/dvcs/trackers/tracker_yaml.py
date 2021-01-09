""" widgets for syncing state with YAML
"""
import yaml

from .tracker_json import JSONDictTracker


class YAMLDictTracker(JSONDictTracker):
    """sync a widget's traits to single YAML file on disk"""

    __extension__ = ".yaml"

    def _read(self, text):
        """read a file with YAML"""
        return yaml.safe_load(text)

    def _write(self, widget_dict):
        """write a file with YAML"""
        return yaml.safe_dump(widget_dict, default_flow_style=False)
