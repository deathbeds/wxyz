""" Widgets for working with State Machines
"""
import ipywidgets.widgets.trait_types as TT
from transitions import Machine

from .base import StateMachineBase, T, W


@W.register
class StateMachine(StateMachineBase):
    """ A Widget that implements a state machine
    """

    _model_name = T.Unicode("StateMachineModel").tag(sync=True)

    states = TT.TypedTuple(trait=T.Unicode(), allow_none=True).tag(sync=True)
    transitions = T.List().tag(sync=True)
    state = T.Unicode(allow_none=True).tag(sync=True)
    initial = T.Unicode().tag(sync=True)
    machine = T.Instance(Machine)

    def _make_machine(self):
        return Machine(
            model=self,
            states=self.states,
            initial=self.initial or (self.states[0] if self.states else None),
            transitions=self.transitions,
        )

    @T.default("machine")
    def _default_machine(self):
        return self._make_machine()

    @T.observe("states", "transitions", "initial")
    def on_configure(self, _):
        """ make a Machine
        """
        self.machine = self._make_machine()
