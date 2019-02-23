from nbconvert.filters.markdown import markdown2html_mistune

from .base import Fn, T, W


@W.register
class Markdown(Fn):
    _model_name = T.Unicode("MarkdownModel").tag(sync=True)

    @T.observe("source")
    def _source_changed(self, *_):
        self.value = markdown2html_mistune(self.source)
