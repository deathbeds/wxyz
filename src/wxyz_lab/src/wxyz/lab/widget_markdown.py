""" Widgets for working with markdown

This module does not yet work in ``jupyterlite``
"""
import mistune

# pylint: disable=import-outside-toplevel
from wxyz.core.base import Fn

from .base import LabBase, T, W


@W.register
class Markdown(Fn, LabBase):
    """A widget that turns markdown source into HTML source"""

    _model_name = T.Unicode("MarkdownModel").tag(sync=True)

    def the_function(self, source):
        """Render some markdown"""
        return mistune.html(source)
