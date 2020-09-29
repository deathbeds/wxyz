""" Jupyter Widgets for fossil
"""
# pylint: disable=no-member

from .base import T
from .widget_repo import Repo


class Fossil(Repo):
    """A git repository"""

    _model_name = T.Unicode("FossilModel").tag(sync=True)
    _view_name = T.Unicode("FossilView").tag(sync=True)
