"""baseline tools for working with time traveling"""

import ipywidgets as W
import jinja2
import traitlets as T

from ..repos.repo_base import Repo

CSS_PREFIX = "jp-wxyz-dvcs-tool-timetravel"

DEFAULT_OPTIONS = [("No History", None)]

DEFAULT_OPTION_TMPL = """
[{{ commit[:7] }}] {{ message }} by {{ author.name }} {{ timestamp }}
""".strip()


class TimeTraveler(W.VBox):
    """Show a selection widget"""

    # pylint: disable=no-self-use,unused-argument
    repo = T.Instance(Repo)
    commits = T.Instance(W.DOMWidget)
    _commits_cls = W.SelectionSlider
    _option_tmpl = jinja2.Template(DEFAULT_OPTION_TMPL)

    def __init__(self, *args, **kwargs):
        if "layout" not in kwargs:
            kwargs["layout"] = dict(
                flex="1",
                display="flex",
            )
        super().__init__(*args, **kwargs)
        T.dlink(
            (self.repo, "head_history"),
            (self.commits, "options"),
            self._update_history_options,
        )
        self._dom_classes += (f"{CSS_PREFIX}-box",)
        self.commits.observe(self._on_change_commit, "value")
        self.children = [self.commits]

    def _on_change_commit(self, change):
        """revert to the selected commit"""
        if change.new:
            self.repo.revert(change.new)

    @T.default("commits")
    def _make_default_commits(self):
        """create a default commit selector"""
        return self._commits_cls(
            options=DEFAULT_OPTIONS,
            description="History",
            layout=dict(width="80%", flex="1"),
        )

    def _update_history_options(self, history):
        """nicely format the commit history"""
        return [(self._option_tmpl.render(**h), h["commit"]) for h in history][
            ::-1
        ] or DEFAULT_OPTIONS
