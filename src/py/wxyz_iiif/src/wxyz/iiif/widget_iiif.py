""" Widgets for working with IIIF
"""
# pylint: disable=too-many-ancestors,no-self-use,too-few-public-methods
# import iiif

from .base import IIIFBase, T, W


@W.register
class IIIF(IIIFBase):
    """ A Widget that parses YAML source into... something
    """

    _model_name = T.Unicode("IIIFModel").tag(sync=True)
    _view_name = T.Unicode("IIIFView").tag(sync=True)
