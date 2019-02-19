from .base import Base
from .base import T
from .base import W


@W.register
class Template(Base):
    _model_name = T.Unicode("TemplateModel").tag(sync=True)

    value = T.Unicode("").tag(sync=True)
    template = T.Unicode("").tag(sync=True)
    context = T.Instance(W.Widget, allow_none=True).tag(
        sync=True, **W.widget_serialization
    )
