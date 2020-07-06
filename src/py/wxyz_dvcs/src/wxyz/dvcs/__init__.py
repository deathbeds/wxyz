""" DVCS widgets
"""
from ._version import __version__  # noqa
from .widget_fossil import Fossil
from .widget_git import Git

__all__ = ["__version__", "Git", "Fossil"]
