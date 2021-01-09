""" Widgets for templating
"""
# pylint: disable=no-self-use
import jinja2

from wxyz.core.base import Fn, T, W

from .base import JinjaBase


@W.register
class Template(Fn, JinjaBase):
    """Transforms text source into text output with a given context"""

    _model_name = T.Unicode("TemplateModel").tag(sync=True)

    context = T.Union([T.Dict(), T.Instance(W.Widget)], allow_none=True).tag(
        sync=True, **W.widget_serialization
    )

    _observed_traits = ["source", "context"]

    @T.observe("context")
    def _context_changed(self, *_):
        """handle connecting to widgets"""
        if self.context and self.context.observe:
            self.context.observe(self.the_observer)

    def the_function(self, source, context):
        """render a source given a context"""
        return jinja2.Template(source).render(context)
