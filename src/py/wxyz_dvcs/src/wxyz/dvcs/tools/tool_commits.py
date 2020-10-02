"""baseline tools for working with commits"""

import ipywidgets as W
import traitlets as T

from ..repos.repo_base import Repo

CSS_PREFIX = "jp-wxyz-dvcs-tool-commit"


class Committer(W.VBox):
    """Create commits with a message"""

    # pylint: disable=no-self-use,unused-argument
    repo = T.Instance(Repo)
    watch = T.Instance(W.DOMWidget)
    message = T.Instance(W.Text)
    commit_btn = T.Instance(W.Button)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # move these into watchers
        T.link((self.watch, "value"), (self.repo, "watching"))
        T.dlink(
            (self.repo, "changes"),
            (self.commit_btn, "description"),
            self.change_btn_desc,
        )
        T.dlink(
            (self.repo, "changes"),
            (self.commit_btn, "disabled"),
            lambda changes: not changes,
        )
        self.commit_btn.on_click(self.commit)
        self._dom_classes += (f"{CSS_PREFIX}-box",)
        self.commit_btn._dom_classes += (f"{CSS_PREFIX}-btn",)
        self.message._dom_classes += (f"{CSS_PREFIX}-msg",)
        self.children = [self.watch, self.message, self.commit_btn]

    def commit(self, *args):
        """actually commit"""
        staged = []
        for change in self.repo.changes:
            for path in ["a_path", "b_path"]:
                if change[path] and change[path] not in staged:
                    self.repo.stage(change[path])
                    staged += [change[path]]
        self.repo.commit(self.message.value or self.message.placeholder)
        self.message.value = ""

    def change_btn_desc(self, changes):
        """update button description"""
        if not changes:
            self.message.placeholder = "Commit message"
            return "No changes"
        paths = sum([[change["a_path"], change["b_path"]] for change in changes], [])
        paths = sorted({p for p in paths if p})
        self.message.placeholder = f"""Updated {", ".join(paths)}"""
        change_plural = "s" if changes and len(changes) >= 2 else ""
        return f"""Commit {len(changes)} change{change_plural}"""

    @T.default("watch")
    def _default_watch(self):
        """default watcher"""

        return W.Checkbox(True, description="Watch")

    @T.default("message")
    def _default_message(self):
        """default message editor"""
        return W.Text(placeholder="Commit Message", description="Log")

    @T.default("commit_btn")
    def _default_commit_btn(self):
        """default commit button"""
        return W.Button(description="Commit")
