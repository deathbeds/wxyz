from .base import Base
from .base import T
from .base import W
from yaml import safe_load


@W.register
class YAML(Base):
    _model_name = T.Unicode("YAMLModel").tag(sync=True)

    source = T.Unicode("").tag(sync=True)
    value = T.Union([T.Dict(), T.List(), T.Unicode(), T.Int(), T.Float()]).tag(
        sync=True
    )

    @T.observe("source")
    def _source_changed(self, *_):
        self.value = safe_load(self.source)
