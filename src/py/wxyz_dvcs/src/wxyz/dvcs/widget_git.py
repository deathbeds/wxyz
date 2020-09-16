""" Jupyter Widgets for git
"""
# pylint: disable=too-many-ancestors,no-member

from .base import T
from .widget_repo import Repo


class Git(Repo):
    """A git repository"""

    _model_name = T.Unicode("GitModel").tag(sync=True)
    _view_name = T.Unicode("GitView").tag(sync=True)
