"""baseline tools for working with remotes"""

# pylint: disable=no-self-use,unused-argument

import ipywidgets as W
import traitlets as T
from tornado.ioloop import IOLoop

from ..repos.repo_base import Repo

CSS_PREFIX = "jp-wxyz-dvcs-tool-remote"


class Remoter(W.VBox):
    """Adds remotes"""

    repo = T.Instance(Repo)
    remote = T.Unicode(allow_none=True)
    head = T.Unicode(allow_none=True)

    remotes = T.Instance(W.DOMWidget)
    heads = T.Instance(W.DOMWidget)
    push_btn = T.Instance(W.Button)
    fetch_btn = T.Instance(W.Button)
    merge_btn = T.Instance(W.Button)

    _remotes_link = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.children = [
            W.HBox([self.remotes, self.fetch_btn]),
            W.HBox([self.heads, self.merge_btn, self.push_btn]),
        ]
        T.dlink((self.remotes, "value"), (self, "remote"))
        T.dlink((self.heads, "value"), (self, "head"))
        T.dlink((self, "remote"), (self.heads, "disabled"), lambda x: not x)
        T.dlink((self, "head"), (self.push_btn, "disabled"), lambda x: not x)

        self.fetch_btn.on_click(self._on_fetch_click)
        self.merge_btn.on_click(self._on_merge_click)

    # handlers
    def _on_fetch_click(self, *args):
        IOLoop.current().add_callback(self.repo.remotes[self.remote].fetch)

    def _on_push_click(self, *args):
        raise NotImplementedError()

    def _on_merge_click(self, *args):
        self.repo.merge(self.heads.value)

    # observers
    @T.observe("repo")
    def _on_repo(self, change):
        """handle the repo changing (including the first time)"""
        if self._remotes_link:
            self._remotes_link.unlink()

        if change.new:
            self._remotes_link = T.dlink(
                (change.new, "remotes"),
                (self.remotes, "options"),
                self._update_remote_options,
            )

    def _update_remote_options(self, remotes):
        """format the remote options (TODO: nicely)"""
        return sorted((remotes))

    def _update_head_options(self, change):
        """format the head options (TODO: nicely)"""
        self.heads.options = tuple(
            sorted(
                [(f"""{head} [{ref[:7]}]""", ref) for head, ref in change.new.items()]
            )
        )

    @T.observe("remote")
    def _on_remote(self, change):
        """handle the current remote name changing"""
        if change.new:
            remote = self.repo.remotes[change.new]
            remote.observe(self._update_head_options, "heads")
        else:
            self.heads.options = []

    # defaults
    @T.default("remotes")
    def _default_remotes(self):
        """initialize the remotes widget"""
        return W.Dropdown(description="Remotes")

    @T.default("heads")
    def _default_heads(self):
        """initialize the heads widget"""
        return W.Dropdown(description="Heads")

    @T.default("fetch_btn")
    def _default_fetch_btn(self):
        """initialize the fetch widget"""
        return W.Button(description="Fetch", icon="cloud-download")

    @T.default("merge_btn")
    def _default_merge_btn(self):
        """initialize the merge widget"""
        return W.Button(description="Merge", icon="compress")

    @T.default("push_btn")
    def _default_push_btn(self):
        """initialize the push widget"""
        return W.Button(description="Push", icon="cloud-upload")
