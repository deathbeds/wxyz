""" Base classes for State Machine
"""
# pylint: disable=unused-import

import ipywidgets as W  # noqa
import traitlets as T

from wxyz.core.base import Base

from ._version import module_name, module_version


class StateMachineBase(Base):
    """ Module metadata for StateMachine
    """

    _model_module = T.Unicode(module_name).tag(sync=True)
    _model_module_version = T.Unicode(module_version).tag(sync=True)
    _view_module = T.Unicode(module_name).tag(sync=True)
    _view_module_version = T.Unicode(module_version).tag(sync=True)
