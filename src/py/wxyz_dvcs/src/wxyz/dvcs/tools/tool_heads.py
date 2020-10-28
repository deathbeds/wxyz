"""baseline tools for working with heads"""

import ipywidgets as W
import traitlets as T
from jinja2 import Template

from ..repos.repo_base import Repo
from .utils import BTN_ICON_DEFAULTS

DEFAULT_STATUS_TEMPLATE = """
<i class="fa fa-code-fork"></i> {{ repo.head }}
<i class="fa fa-hashtag"></i>
<code title="{{repo.head_hash}}">{{ repo.head_hash[:7] }}</code>
{% if repo.changes %}
<i class="fa fa-pencil-square"></i> {{ repo.changes | count }} changes
{% endif %}
"""


class HeadStatus(W.HBox):
    """a status bar"""

    # pylint: disable=fixme,no-self-use

    repo = T.Instance(Repo)
    # todo: break up more for styling
    html = T.Instance(W.HTML, kw={})
    template = T.Instance(Template)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.children = [self.html]
        # todo: handle repo change
        self.repo.observe(self._on_repo_update)

    def _on_repo_update(self, _change):
        """update the status bar"""
        self.html.value = self.template.render(repo=self.repo)

    @T.default("template")
    def _default_template(self):
        """make a default template"""
        return Template(DEFAULT_STATUS_TEMPLATE)


class HeadPicker(W.HBox):
    """a simple dropdown-based picker of current DVCS heads"""

    # pylint: disable=no-self-use,unused-argument

    repo = T.Instance(Repo)
    picker = T.Instance(W.DOMWidget)
    refresh_btn = T.Instance(W.Button)
    checkout_btn = T.Instance(W.Button)

    _repo_link = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.refresh_btn.on_click(self.refresh)
        self.checkout_btn.on_click(self.checkout)
        self.picker.observe(self._update_picker_value, "options")
        self.children = [self.picker, self.refresh_btn, self.checkout_btn]

    def refresh(self, *args, **kwargs):
        """refresh the heads"""
        # pylint: disable=protected-access
        if self.repo is not None:
            self.repo._update_heads()

    def checkout(self, *args, **kwargs):
        """check out a ref"""
        self.repo.checkout(self.picker.value)

    def _update_picker_value(self, *args, **kwargs):
        """ensure the right option is selected"""
        self.picker.value = self.repo.head

    @T.observe("repo")
    def _on_repo_changed(self, change):
        """react to the repo changing"""
        if self._repo_link is not None:
            self._repo_link.unlink()
            self._repo_link = None

        if change.new:
            self._repo_link = T.dlink(
                (change.new, "heads"),
                (self.picker, "options"),
                self._format_head_options,
            )

    def _format_head_options(self, heads):
        marks = {self.repo.head: "*"}
        return {
            f"""{marks.get(name, "")}{name} [{commit[:7]}]""": name
            for name, commit in heads.items()
        }

    @T.default("picker")
    def _default_picker(self):
        """a default picker"""
        return W.Dropdown(description="Head")

    @T.default("refresh_btn")
    def _default_refresh_btn(self):
        """a default refresh button"""
        return W.Button(icon="refresh", **BTN_ICON_DEFAULTS)

    @T.default("checkout_btn")
    def _default_checkout_btn(self):
        """a default checkout button"""
        return W.Button(icon="check-circle", **BTN_ICON_DEFAULTS)


class Brancher(W.HBox):
    """Create a new branch from the current commit"""

    # pylint: disable=no-self-use,unused-argument

    repo = T.Instance(Repo)
    create_btn = T.Instance(W.Button)
    branch_name = T.Instance(W.Text)

    _repo_link = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_btn.on_click(self.create)
        T.dlink(
            (self.branch_name, "value"), (self.create_btn, "disabled"), lambda x: not x
        )
        self.children = [self.branch_name, self.create_btn]

    def create(self, *args, **kwargs):
        """actually create the new branch"""
        self.repo.branch(self.branch_name.value)
        self.branch_name.value = ""

    @T.default("create_btn")
    def _default_create_btn(self):
        """a default create button"""
        return W.Button(icon="plus", **BTN_ICON_DEFAULTS)

    @T.default("branch_name")
    def _default_branch_name(self):
        """a default branch name editor"""
        return W.Text(description="New Branch")
