""" Widgets for working with State Machines
"""
# pylint: disable=fixme,no-member,broad-except
import ipywidgets.widgets.trait_types as TT
from transitions import Machine
from transitions.extensions import MachineFactory

from .base import StateMachineBase, T, W

NO_PYGRAPHVIZ = False

try:
    __import__("pygraphviz")
except ImportError:
    NO_PYGRAPHVIZ = True


class _StateModel(T.HasTraits):
    # TODO: support the State object natively, especially on_*
    state = T.Unicode(allow_none=True).tag(sync=True)


@W.register
class StateMachine(StateMachineBase):
    """ A Widget that implements a state machine

        https://github.com/pytransitions/transitions#basic-initialization
    """

    _Machine = Machine

    _model_name = T.Unicode("StateMachineModel").tag(sync=True)

    states = TT.TypedTuple(trait=T.Unicode(), allow_none=True).tag(sync=True)

    transitions = T.List().tag(sync=True)

    # TODO: support the State object natively, especially on_*
    state = T.Unicode(allow_none=True).tag(sync=True)

    initial = T.Unicode().tag(sync=True)
    machine = T.Instance(Machine, allow_none=True)
    nested = T.Bool(False).tag(sync=True)
    graph = T.Bool(False).tag(sync=True)
    locked = T.Bool(False).tag(sync=True)
    svg = T.Unicode("").tag(sync=True)
    prog = T.Unicode("dot").tag(sync=True)

    model = T.Instance(_StateModel)

    def _update_svg(self):
        if self.graph and self.machine and self.model and not NO_PYGRAPHVIZ:
            try:
                self.svg = self.model.get_graph().draw(format="svg", prog=self.prog)
                self.error = ""
            except Exception as err:
                self.error = str(err)
                self.svg = ""

    def _make_machine(self):
        model = self.model = _StateModel()

        machine = MachineFactory.get_predefined(
            nested=self.nested, graph=self.graph, locked=self.locked
        )(
            model=model,
            states=self.states,
            initial=self.initial or (self.states[0] if self.states else None),
            transitions=self.transitions,
        )

        T.dlink((model, "state"), (self, "state"))

        def maybe_update(*_):
            if machine == self.machine:
                machine.set_state(self.state)

        self.observe(maybe_update, "state")

        return machine

    @T.observe("state")
    def _on_changing_state(self, _):
        self._update_svg()

    @T.default("machine")
    def _default_machine(self):
        return self._make_machine()

    @T.observe("states", "transitions", "initial")
    def on_configure(self, _):
        """ make a Machine
        """
        self.machine = self._make_machine()
        self._update_svg()
