""" base classes for changes on disk to widgets
"""
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import ipywidgets as W
import ipywidgets.embed as E
import traitlets as T
from tornado.concurrent import run_on_executor
from tornado.ioloop import IOLoop


class Tracker(W.Widget):
    """base class for trackers"""

    # pylint: disable=unused-argument,no-member
    tracked_widget = T.Instance(W.Widget)
    tracked_traits = W.trait_types.TypedTuple(
        T.Unicode(), allow_none=True, help="trait names to track (default all)"
    )
    path = T.Instance(Path)
    encoding = T.Unicode("utf-8")
    user_idle_interval = T.Float(
        0.3, help="seconds to wait before declaring the user idle"
    )
    _idle_after = None
    __extension__ = None

    @property
    def loop(self):
        """get the current event loop, if available"""
        try:
            return IOLoop.current()
        except RuntimeError:
            return None

    async def on_user_change(self):
        """react to a user changing a widget"""
        raise NotImplementedError(
            "tracker subclass must implement `async on_user_change`"
        )

    async def on_file_change(self):
        """react to a file changing on disk"""
        raise NotImplementedError(
            "tracker subclass must implement `async on_user_change`"
        )

    def _on_user_change(self, change):
        """bridge to the ioloop for user changes, handle idle"""
        loop = self.loop
        self._idle_after = time.time() + self.user_idle_interval
        if loop is not None:
            loop.add_callback(self.on_user_change)

    def _on_file_change(self, change):
        """bridge to the ioloop for file changes (if the user isn't interacting)"""
        loop = self.loop
        if self._idle_after and time.time() < self._idle_after:
            return
        if loop is not None:
            loop.add_callback(self.on_file_change)

    @T.observe("tracked_widget")
    def _changed_tracked_widget(self, change):
        """handle the widget changing"""
        if change.old is not None and isinstance(change.old, W.Widget):
            change.old.unobserve(self._on_user_change, self.tracked_traits or T.All)
        if change.new is not None:
            change.new.observe(self._on_user_change, self.tracked_traits or T.All)
            self._on_file_change(None)

    @T.observe("tracked_traits")
    def _changed_tracked_traits(self, change):
        """handle the tracked traits changing"""

        if self.tracked_widget is None or not isinstance(self.tracked_widget, W.Widget):
            return
        if change.old is None or isinstance(change.old, tuple):
            self.tracked_widget.unobserve(self._on_user_change, change.old or T.All)
        if change.new is None or isinstance(change.new, tuple):
            self.tracked_widget.observe(self._on_user_change, change.new or T.All)
            self._on_file_change(None)

    @classmethod
    def detect_tracker(cls, path, base_cls=None):
        """naive tracker finder... needs something cleverer"""
        base_cls = base_cls or Tracker

        if base_cls.__extension__ and path.name.endswith(base_cls.__extension__):
            return base_cls

        subclasses = base_cls.__subclasses__()

        for sub_cls in subclasses:
            if sub_cls.__extension__ and path.name.endswith(sub_cls.__extension__):
                return sub_cls

        for sub_cls in subclasses:
            subsub = cls.detect_tracker(path, sub_cls)
            if subsub:
                return subsub

        return None


class DictTracker(Tracker):
    """tracker which serializes to a dictionary/map/hash"""

    # pylint: disable=abstract-method
    def dict_from_widget(self):
        """generate a JSON-ready dict from a widget"""
        d = {}
        w = self.tracked_widget
        if w is not None:
            s = E.dependency_state(w)[w.comm.comm_id]["state"]
            for k in self.tracked_traits or list(s):
                d[k] = s.get(k, None)
        return d

    def widget_from_dict(self, content):
        """update a widget from a dict"""
        with self.tracked_widget.hold_trait_notifications():
            for trait_name in self.tracked_traits or self.tracked_widget.trait_names():
                if trait_name in content:
                    trait = getattr(self.tracked_widget.__class__, trait_name)
                    new_value = content[trait_name]
                    old_value = getattr(self.tracked_widget, trait_name)
                    from_json = trait.metadata.get("from_json")
                    to_json = trait.metadata.get("to_json")
                    if to_json and from_json:
                        if new_value == to_json(old_value, self.tracked_widget):
                            continue
                        setattr(
                            self.tracked_widget,
                            trait_name,
                            from_json(new_value, self.tracked_widget),
                        )
                    else:
                        if old_value != new_value:
                            setattr(
                                self.tracked_widget,
                                trait_name,
                                new_value,
                            )


class ExecutorTracker(Tracker):
    """base class for wrapping synchronous file IO
    use this for the currently relatively common case of serialization
    libraries that have blocking IO
    """

    executor = ThreadPoolExecutor(max_workers=1)

    @run_on_executor
    def on_user_change_sync(self):
        """do file writing on a thread"""
        raise NotImplementedError(
            "tracker subclass must implement `on_user_change_sync`"
        )

    @run_on_executor
    def on_file_change_sync(self):
        """do file reading on a thread"""
        raise NotImplementedError(
            "tracker subclass must implement `on_file_change_sync`"
        )

    async def on_user_change(self):
        """react to a user change"""
        await self.on_user_change_sync()

    async def on_file_change(self):
        """react to a file change"""
        await self.on_file_change_sync()
