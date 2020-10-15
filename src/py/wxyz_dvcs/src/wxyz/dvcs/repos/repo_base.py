""" base DVCS repository widgets
"""
from concurrent.futures import ThreadPoolExecutor

# pylint: disable=no-member
from pathlib import Path

import ipywidgets as W
import traitlets as T
from tornado.ioloop import IOLoop

from ..trackers.tracker_base import Tracker
from ..widget_watch import Watcher


class Remote(W.Widget):
    """a remote DVCS repository"""

    name = T.Unicode()
    url = T.Unicode()
    heads = T.Dict(value_trait=T.Unicode(), default_value=tuple())
    auto_fetch = T.Bool(True)

    executor = ThreadPoolExecutor(max_workers=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.auto_fetch:
            self._on_auto_fetch()

    async def fetch(self):
        """fetch from the remote"""
        await self._fetch()
        self.heads = await self._update_heads()

    async def push(self, ref):
        """push to the remote"""
        await self._push(ref)

    @T.observe("auto_fetch")
    def _on_auto_fetch(self, _change=None):
        """handle changing the auto fetch preference"""
        if self.auto_fetch:
            IOLoop.current().add_callback(self.fetch)


class Repo(W.Widget):
    """base class for a DVCS repo"""

    executor = ThreadPoolExecutor(max_workers=1)

    # pylint: disable=no-self-use,unused-argument
    working_dir = T.Instance(Path)
    url = T.Unicode()
    watching = T.Bool(default_value=False)
    dirty = T.Bool(default_value=False)
    changes = T.Tuple(allow_none=True)
    head = T.Unicode(help="the symbolic name of the current head")
    head_hash = T.Unicode(help="the full hash of the current head")
    head_history = T.Tuple()
    remotes = T.Dict(value_trait=T.Instance(Remote), default_value=tuple())
    _remote_cls = Remote

    heads = T.Dict(value_trait=T.Unicode(), default_value=tuple())
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

    def add_remote(self, name, url, **kwargs):
        """add a new reference to a remote repository"""
        self._update_remotes()
        remotes = dict(self.remotes)
        old_remote = remotes.get(name)
        if old_remote is None:
            remotes[name] = self._remote_cls(local=self, name=name, url=url, **kwargs)
        else:
            old_remote.url = url
        self.remotes = remotes
