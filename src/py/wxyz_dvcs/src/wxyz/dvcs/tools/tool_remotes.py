"""baseline tools for working with remotes"""

# pylint: disable=no-self-use

import ipywidgets as W
import traitlets as T

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

    _remotes_link = None
    _heads_link = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.children = [self.remotes, self.heads, self.fetch_btn, self.push_btn]
        T.dlink((self.remotes, "value"), (self, "remote"))
        T.dlink((self.heads, "value"), (self, "head"))
        T.dlink((self, "remote"), (self.heads, "disabled"), lambda x: not x)
        T.dlink((self, "head"), (self.push_btn, "disabled"), lambda x: not x)

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
        """format the remote options (nicely)"""
        return sorted(remotes)

    @T.observe("remote")
    def _on_remote(self, change):
        """handle the current remote name changing"""
        if self._heads_link:
            self._heads_link.unlink()
            self._heads_link = None

        if change.new and self.repo and change.new in self.repo.remotes:
            self.heads.options = self.repo.remotes[change.new].heads
            self._heads_link = T.dlink(
                (self.repo.remotes[change.new], "heads"), (self.heads, "options")
            )
        else:
            self.heads.options = []

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
        return W.Button(icon="cloud-download")

    @T.default("push_btn")
    def _default_push_btn(self):
        """initialize the push widget"""
        return W.Button(icon="cloud-upload")
