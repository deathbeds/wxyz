from .base import Base
from .base import T
from .base import W
from nbconvert.filters.markdown import markdown2html_mistune


@W.register
class Markdown(Base):
    _model_name = T.Unicode("MarkdownModel").tag(sync=True)

    source = T.Unicode("").tag(sync=True)
    value = T.Unicode("").tag(sync=True)

    @T.observe("source")
    def _source_changed(self, *_):
        self.value = markdown2html_mistune(self.source)
