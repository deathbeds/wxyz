from collections import defaultdict

import jinja2

from .base import Fn, T, W


@W.register
class Template(Fn):
    _model_name = T.Unicode("TemplateModel").tag(sync=True)

    context = T.Union([
            T.Dict(), T.Instance(W.Widget)
        ], allow_none=True).tag(
        sync=True, **W.widget_serialization
    )

    @T.observe("context")
    def _context_changed(self, *_):
        if self.context:
            self.context.observe(self._source_changed)

    @T.observe("source")
    def _source_changed(self, *_):
        try:
            self.value = jinja2.Template(self.source).render(
                self.context._trait_values if self.context else defaultdict(lambda: "")
            )
            self.error = ""
        except Exception as err:
            self.error = str(err)
