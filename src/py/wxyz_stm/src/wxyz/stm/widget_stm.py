""" Widgets for working with State Machines
"""
# pylint: disable=fixme,no-member,broad-except
import ipywidgets.widgets.trait_types as TT
from transitions import Machine, State
from transitions.extensions import MachineFactory

from .base import StateMachineBase, T, W

NO_PYGRAPHVIZ = False

try:
    __import__("pygraphviz")
except ImportError:
    NO_PYGRAPHVIZ = True


class _StateMachineModel(T.HasTraits):
    # TODO: support the State object natively, especially on_*
    state = T.Unicode(allow_none=True).tag(sync=True)


@W.register
class StateMachine(StateMachineBase):
    """ A Widget that implements a state machine

        https://github.com/pytransitions/transitions#basic-initialization
    """

    _Machine = Machine

    _model_name = T.Unicode("StateMachineModel").tag(sync=True)

    states = T.List().tag(sync=True)
    initial = T.Unicode().tag(sync=True)
    transitions = T.List().tag(sync=True)

    machine = T.Instance(Machine, allow_none=True)
    model = T.Instance(_StateMachineModel)

    state = T.Unicode(allow_none=True).tag(sync=True)

    def make_machine(self):
        model = self.model = _StateMachineModel()

        machine = MachineFactory.get_predefined(**self.machine_factory_args())(
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

    def machine_factory_args(self):
        return dict(nested=True)

    @T.default("machine")
    def _default_machine(self):
        return self.make_machine()

    @T.observe("states", "transitions", "initial", "locked", "nested")
    def on_configure(self, _):
        """ make a Machine
        """
        self.machine = self.make_machine()


@W.register
class GraphMachine(StateMachine):
    """ A Widget that implements a state machine with SVG support
    """

    _model_name = T.Unicode("GraphMachineModel").tag(sync=True)

    svg = T.Unicode("").tag(sync=True)
    prog = T.Unicode("dot").tag(sync=True)

    def _update_svg(self):
        try:
            self.svg = self.model.get_graph().draw(format="svg", prog=self.prog)
            self.error = ""
        except Exception as err:
            self.error = str(err)
            self.svg = ""

    @T.observe("state")
    def _on_changing_state(self, _):
        self._update_svg()

    def machine_factory_args(self):
        args = dict(graph=True)
        args.update(super().machine_factory_args())
        return args

    def make_machine(self):
        machine = super().make_machine()
        self._update_svg()
        return machine

    @T.observe("prog")
    def on_configure_prog(self, _):
        """ make a Machine
        """
        self.machine = self.make_machine()
        self._update_svg()
