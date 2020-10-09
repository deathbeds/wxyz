""" base DVCS repository widgets
"""
# pylint: disable=no-member
from pathlib import Path

import ipywidgets as W
import traitlets as T

from ..trackers.tracker_base import Tracker
from ..widget_watch import Watcher


class Repo(W.Widget):
    """base class for a DVCS repo"""

    # pylint: disable=no-self-use,unused-argument
    working_dir = T.Instance(Path)
    url = T.Unicode()
    watching = T.Bool(default_value=False)
    dirty = T.Bool(default_value=False)
    changes = T.Tuple(allow_none=True)
    head = T.Unicode()
    head_history = T.Tuple()
    heads = W.trait_types.TypedTuple(T.Unicode(), default_value=tuple())
    _watcher = T.Instance(Watcher, allow_none=True)
    _trackers = W.trait_types.TypedTuple(T.Instance(Tracker), default_value=tuple())
    _change_link = None

    def __init__(self, working_dir, *args, **kwargs):
        kwargs["working_dir"] = Path(kwargs.get("working_dir", working_dir))
        super().__init__(*args, **kwargs)
        T.dlink((self, "working_dir"), (self, "url"), lambda p: p.resolve().as_uri())

    @T.default("changes")
    def _default_changes(self):
        """nothing should have changed by default"""
        return tuple()

    @T.observe("watching", "path")
    def _on_watching(self, change):
        """react to the watch state (or path) changing"""
        if self._watcher:
            if self._change_link:
                self._change_link.unlink()
                self._change_link = None
            self._watcher.watching = False
            self._watcher = None
        if self.watching:
            self._watcher = Watcher(self.working_dir)
            self._change_link = T.dlink(
                (self._watcher, "changes"), (self, "changes"), self._on_watch_changes
            )
            self._watcher.watching = True

    def _on_watch_changes(self, changes):
        """react to changes from the watcher"""
        self.log.warn("changes %s", changes)
        return changes

    def track(self, **kwargs):
        """create a tracker for the given widget"""
        assert self.working_dir.exists()
        kwargs["path"] = Path(self.working_dir / kwargs["path"])
        tracker_cls = kwargs.pop("tracker_cls", None)
        if tracker_cls is None:
            tracker_cls = Tracker.detect_tracker(kwargs["path"])
        assert tracker_cls is not None
        tracker = tracker_cls(**kwargs)
        self._trackers += (tracker,)
        return tracker


class Remote(W.Widget):
    """a remote DVCS repository"""

    name = T.Unicode()
    url = T.Unicode()
    local = T.Instance(Repo)

    async def fetch(self):
        """fetch from the remote"""
        raise NotImplementedError(f"{self.__class__} needs to implement fetch")

    async def push(self, ref):
        """push to the remote"""
        raise NotImplementedError(f"{self.__class__} needs to implement fetch")
