""" widgets for syncing state with JSON
"""

import json

from tornado.concurrent import run_on_executor

from .tracker_base import DictTracker, ExecutorTracker


class JSONDictTracker(DictTracker, ExecutorTracker):
    """sync a widget's traits to single JSON file on disk"""

    # pylint: disable=no-self-use
    __extension__ = ".json"

    def _read(self, text):
        return json.loads(text)

    def _write(self, widget_dict):
        return json.dumps(widget_dict, sort_keys=True, indent=True)

    @run_on_executor
    def on_user_change_sync(self):
        """perform JSON writing on thread"""
        self.path.write_text(
            self._write(self.dict_from_widget()),
            encoding=self.encoding,
        )

    @run_on_executor
    def on_file_change_sync(self):
        """perform JSON reading in thread"""
        if self.path.exists():
            self.widget_from_dict(self._read(self.path.read_text(encoding="utf-8")))
