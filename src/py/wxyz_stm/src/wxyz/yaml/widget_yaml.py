""" Widgets for working with State Machines
"""
# pylint: disable=too-many-ancestors,no-self-use,too-few-public-methods
from wxyz.core.widget_json import JSON

from .base import T, W, StateMachineBase

from transitions import Machine


@W.register
class StateMachine(StateMachineBase):
    """ A Widget that parses State Machine source into... something
    """

    _model_name = T.Unicode("StateMachineModel").tag(sync=True)

    states = W.trait_types.TypedTuple(trait=T.Unicode()).tag(sync=True)
    transitions = W.trait_types.TypedTuple(trait=T.Dict()).tag(sync=True)
    machine = T.Instance(Machine)
    state = T.Unicode().tag(sync=True)

    @T.observe("states", "transitions")
    def on_configure(self, _):
        """ make a Machine
        """
        self.machine = Machine(
            Machine(
                model=self,
                states=self.states,
                initial=self.initial or self.states[0],
                transitions=self.transitions
            )
        )
