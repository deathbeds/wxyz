from .base import Base
from .base import T
from .base import W

import json


@W.register
class JSON(Base):
    _model_name = T.Unicode("JSONModel").tag(sync=True)

    source = T.Unicode("").tag(sync=True)
    value = T.Union([T.Dict(), T.List(), T.Unicode(), T.Int(), T.Float()]).tag(
        sync=True
    )

    @T.observe("source")
    def _source_changed(self, *_):
        self.value = json.loads(self.source)
