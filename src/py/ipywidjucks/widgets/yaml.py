import yaml

from .base import Base, T, W


@W.register
class YAML(Base):
    _model_name = T.Unicode("YAMLModel").tag(sync=True)

    value = T.Union([T.Dict(), T.List(), T.Unicode(), T.Int(), T.Float()]).tag(
        sync=True
    )

    @T.observe("source")
    def _source_changed(self, *_):
        self.value = yaml.safe_load(self.source)
