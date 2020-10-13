""" widgets for watching files
"""
import time

# pylint: disable=no-self-use,keyword-arg-before-vararg
from asyncio import Event
from pathlib import Path

import ipywidgets as W
import traitlets as T
from tornado.ioloop import IOLoop
from watchgod import DefaultDirWatcher, awatch


class _JupyterWatcher(DefaultDirWatcher):
    """a notebook-aware watcher

    TODO: this will need to be revisited... we might in fact want to watch
    more things
    """

    def should_watch_dir(self, entry):
        if not super().should_watch_dir(entry):
            return False
        return ".ipynb_checkpoints" not in str(entry)


class Watcher(W.Widget):
    """A lightweight watcher

    TODO: expose more bits
    """

    path = T.Instance(Path, help="the root path to watch")
    watching = T.Bool(default_value=False, help="whether to be watching")
    changes = T.Tuple(help="the last changes that were detected", allow_none=True)
    _stop = T.Instance(Event, allow_none=True, help="the event to use for stopping")
    _watcher_cls = T.Any(default_value=_JupyterWatcher)

    def __init__(self, path=None, *args, **kwargs):
        kwargs["path"] = kwargs.get("path", Path(path))
        super().__init__(*args, **kwargs)

    @T.default("changes")
    def _default_changes(self):
        return tuple()

    @T.observe("watching", "path")
    def _on_watching(self, change):
        """handle starting/stopping the watcher"""
        if self._stop is not None:
            self._stop.set()
            self.changes = None
            self._stop = None

        if change.new:
            IOLoop.current().add_callback(self._watch)

    def _changes(self, changes):
        """publish the changes. schedule to run in the loop"""
        self.changes = [
            {
                "change": k.name,
                "path": str(Path(v).relative_to(self.path)),
                "time": time.time(),
            }
            for k, v in sorted(changes)
        ]

    async def _watch(self):
        """the actual watcher. schedule to run in the loop"""
        self._stop = Event()
        async for changes in awatch(
            self.path, watcher_cls=self._watcher_cls, stop_event=self._stop
        ):
            IOLoop.current().add_callback(self._changes, changes)
