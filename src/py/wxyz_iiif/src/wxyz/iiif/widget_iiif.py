""" Widgets for working with IIIF
"""
# pylint: disable=too-many-ancestors,no-self-use,too-few-public-methods,no-member
# import iiif

from .base import IIIFBase, T, W


class Manifest(IIIFBase):
    """ An IIIF Manifest
    """

    _model_name = T.Unicode("ManifestModel").tag(sync=True)
    url = T.Unicode(allow_none=True).tag(sync=True)
    value = T.Dict(allow_none=True).tag(sync=True)
    fetching = T.Bool().tag(sync=True)


@W.register
class IIIF(IIIFBase, W.Box):
    """ A Widget that shows IIIF with... something
    """

    _model_name = T.Unicode("IIIFModel").tag(sync=True)
    _view_name = T.Unicode("IIIFView").tag(sync=True)

    manifests = W.trait_types.TypedTuple(trait=T.Instance(Manifest)).tag(
        sync=True, **W.widget_serialization
    )

    @T.default("manifests")
    def _default_manifests(self):
        return []
