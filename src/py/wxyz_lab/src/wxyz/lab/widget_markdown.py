""" Widgets for working with markdown
"""
# pylint: disable=no-self-use
from nbconvert.filters.markdown import markdown2html_mistune

# pylint: disable=too-many-ancestors
from .base import LabBase, T, W
from wxyz.core.base import Fn


@W.register
class Markdown(Fn, LabBase):
    """ A widget that turns markdown source into HTML source
    """

    _model_name = T.Unicode("MarkdownModel").tag(sync=True)

    def the_function(self, source):
        """ Render some Jupyter markdown
        """
        return markdown2html_mistune(source)
