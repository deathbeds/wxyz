""" DVCS widgets
"""
from ._version import __version__  # noqa
from .widget_fossil import Fossil
from .widget_git import Git
from .widget_watch import Watcher

__all__ = ["__version__", "Git", "Fossil", "Watcher"]
