""" a widgetful wrapper around gitpython
"""
from pathlib import Path

import git as G
import traitlets as T
from tornado.concurrent import run_on_executor
from tornado.ioloop import IOLoop
from watchgod import DefaultDirWatcher

from ..widget_watch import Watcher
from .repo_base import Remote, Repo


class _GitRefWatcher(DefaultDirWatcher):
    """a permissive watcher"""

    def should_watch_dir(self, entry):
        """should already be scoped"""
        return True


class GitRemote(Remote):
    """ a git remote """

    local = T.Instance(Repo)
    _remote = T.Instance(G.Remote, allow_none=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._remote is None:
            self._remote = self.local._git.create_remote(self.name, self.url)

    @run_on_executor
    def _fetch(self):
        self._remote.fetch()

    @run_on_executor
    def _update_heads(self):
        heads = {ref.remote_head: str(ref.commit) for ref in self._remote.refs}
        return heads

    async def push(self, ref=None):
        raise NotImplementedError("no push for you")


class Git(Repo):
    """A git repository widget"""

    # pylint: disable=protected-access,too-many-instance-attributes
    _git = T.Instance(G.Repo, allow_none=True)
    _ref_watcher = T.Instance(Watcher, allow_none=True)

    def _initialize_watcher(self):
        """watch key folders in git"""
        self._watcher = Watcher(
            Path(self._git.git_dir) / "refs", _watcher_cls=_GitRefWatcher
        )

        def _schedule(change=None):
            IOLoop.current().add_callback(self._on_ref_change, change)

        self._watcher.observe(_schedule, "changes")

        _schedule()

    async def _on_ref_change(self, _change=None):
        """recalculate key values when files in .git/refs folder change"""
        self._update_heads()
        self._update_head_history()
        for remote in self.remotes.values():
            await remote._update_heads()

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

            self._initialize_watcher()
            self._update_head_history()

    @T.default("head")
    def _default_head(self):
        """get current head"""
        return self._git.active_branch.name

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
            self.head_hash = head.commit.hexsha
            self.head_history = [
                {
                    "commit": str(c.newhexsha),
                    "timestamp": c.time[0],
                    "message": c.message,
                    "author": {"name": c.actor.name, "email": c.actor.email},
                }
                for c in head.log()[::-1]
            ]
        except Exception as err:
            self.log.warn("Git head update error, ignoring: %s", err, exc_info=True)
            self.head_history = []

    def _update_heads(self):
        """refresh the heads"""
        self.heads = {head.name: head.commit.hexsha for head in self._git.heads}
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

    def revert(self, ref):
        """restore to a committish"""
        self._git.head.commit = ref
        self._git.head.reset(index=True, working_tree=True)

    def branch(self, name, ref="HEAD"):
        """create and checkout a new branch"""
        self._git.create_head(name, ref)
        self.checkout(name)

    def checkout(self, name):
        """checkout a named reference"""
        head = [h for h in self._git.heads if h.name == name][0]
        head.checkout()
        self.head = head.name
        self._git.head.reset(index=True, working_tree=True)

    def merge(self, ref):
        """create a merge commit on the active branch with the given ref"""
        active = self._git.active_branch
        active_commit = self._git.active_branch.commit
        active_name = active.name
        merge_base = self._git.merge_base(active, ref)
        ref_commit = self._git.commit(ref)
        self._git.index.merge_tree(ref_commit, base=merge_base)
        merge_commit = self._git.index.commit(
            f"Merged {ref} into {active_name}",
            parent_commits=(active_commit, ref_commit),
        )
        self.log.error("MERGE %s", merge_commit)
        self._git.active_branch.reference = merge_commit
        active.checkout()
        self._git.head.reset(index=True, working_tree=True)

    def _update_remotes(self):
        """fetch some remotes"""
        remotes = {}
        for remote in self._git.remotes:
            remotes[remote.name] = self._remote_cls(
                name=remote.name, url=remote.url, _remote=remote
            )
        self.remotes = remotes
