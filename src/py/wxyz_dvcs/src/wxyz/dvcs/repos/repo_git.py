""" a widgetful wrapper around gitpython
"""
from pathlib import Path

import git as G
import traitlets as T
from tornado.concurrent import run_on_executor

from .repo_base import Remote, Repo


class GitRemote(Remote):
    """ a git remote """

    local = T.Instance(Repo)
    _remote = T.Instance(G.Remote)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._remote = self.local._git.create_remote(self.name, self.url)

    @run_on_executor
    def _fetch(self):
        self._remote.fetch()

    @run_on_executor
    def _update_heads(self):
        return [ref.remote_head for ref in self._remote.refs]

    async def push(self, ref=None):
        raise NotImplementedError("no push for you")


class Git(Repo):
    """A git repository widget"""

    # pylint: disable=protected-access
    _git = T.Instance(G.Repo, allow_none=True)

    @property
    def _remote_cls(self):
        return GitRemote

    @T.observe("working_dir")
    def _on_path(self, change):
        """handle when the working directory changes"""
        if change.new:
            self._git = G.Repo.init(change.new)
            ignore = Path(change.new) / ".gitignore"
            if not ignore.exists():
                ignore.write_text(".ipynb_checkpoints/")
                self.commit("initial commit")
            self._update_head_history()

    @T.default("head")
    def _default_head(self):
        """get current head"""
        return self._git.head.name

    @T.observe("head")
    def _on_head_changed(self, change):
        """react to the symbolic head name changing"""
        if change.new:
            self._update_head_history()

    def _update_head_history(self):
        """build a structure of history"""
        # pylint: disable=broad-except
        try:
            head = [h for h in self._git.heads if h.name == self.head][0]
            self.head_history = [
                {
                    "commit": c.newhexsha,
                    "timestamp": c.time[0],
                    "message": c.message,
                    "author": {"name": c.actor.name, "email": c.actor.email},
                }
                for c in head.log()[::-1]
            ]
        except Exception as err:
            self.log.warn(err)
            self.head_history = []

    def _update_heads(self):
        """refresh the heads"""
        self.heads = [head.name for head in self._git.heads]
        if self.head in [None, "HEAD"] and self.heads:
            self.head = "master"

        self._update_head_history()

    def _on_watch_changes(self, *changes):
        """overload of the base method to handle changes"""
        self.dirty = self._git.is_dirty()
        if self._watcher:
            for change in self._watcher.changes:
                for tracker in self._trackers:
                    tracked_path = Path(self._git.working_dir) / change["path"]
                    if tracker.path.resolve() == tracked_path.resolve():
                        tracker._on_file_change(None)
        return [
            dict(a_path=diff.a_path, b_path=diff.b_path, change_type=diff.change_type)
            for diff in self._git.index.diff(None)
        ] + [
            dict(a_path=None, b_path=ut, change_type="U")
            for ut in self._git.untracked_files
        ]

    def stage(self, path):
        """stage a single path to the index"""
        self._git.index.add(path)

    def unstage(self, path):
        """remove a path from the index"""
        self._git.index.remove(path)

    def commit(self, message):
        """create a commit"""
        self._git.index.commit(message)
        self._on_watching(None)
        self._update_heads()

    def revert(self, ref):
        """restore to a committish"""
        self._git.head.commit = ref
        self._git.head.reset(index=True, working_tree=True)
        self._update_heads()
