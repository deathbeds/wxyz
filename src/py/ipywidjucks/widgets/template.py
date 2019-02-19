from .base import Base, W


class Template(Base):
    _model_name = T.Unicode('TemplateModel').tag(sync=True)

    value = T.Unicode('').tag(sync=True)
    template = T.Unicode('').tag(sync=True)
    context = T.Instance(W.Widget).tag(sync=True)
