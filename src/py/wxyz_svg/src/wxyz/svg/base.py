""" Base classes for SVG
"""
# pylint: disable=unused-import
import ipywidgets as W  # noqa
import traitlets as T

from wxyz.core.base import Base

from ._version import module_name, module_version


class SVGBase(Base):
    """Module metadata for SVG"""

    _model_module = T.Unicode(module_name).tag(sync=True)
    _model_module_version = T.Unicode(module_version).tag(sync=True)
    _view_module = T.Unicode(module_name).tag(sync=True)
    _view_module_version = T.Unicode(module_version).tag(sync=True)
