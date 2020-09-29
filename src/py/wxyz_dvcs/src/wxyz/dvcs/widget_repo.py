""" Jupyter Widgets for any DVCS
"""
# pylint: disable=no-member

from pathlib import Path

from .base import DVCSBase, T, W


@W.register
class Remote(DVCSBase):
    """A remote"""

    _model_name = T.Unicode("RemoteModel").tag(sync=True)
    _view_name = T.Unicode("RemoteView").tag(sync=True)


@W.register
class User(DVCSBase):
    """A user"""

    email = T.Unicode().tag(sync=True)
    name = T.Unicode().tag(sync=True)


@W.register
class Repo(DVCSBase):
    """A repo"""

    _model_name = T.Unicode("RepoModel").tag(sync=True)
    _view_name = T.Unicode("RepoView").tag(sync=True)
    path = T.Instance(Path)


@W.register
class Workspace(DVCSBase):
    """A checked out repository"""

    _model_name = T.Unicode("WorkspaceModel").tag(sync=True)
    _view_name = T.Unicode("WorkspaceView").tag(sync=True)
    repo = T.Instance(Repo).tag(**W.widget_serialization)
    path = T.Instance(Path)
