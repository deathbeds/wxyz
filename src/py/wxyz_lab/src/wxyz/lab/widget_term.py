""" Terminal viewing widgets
"""
# pylint: disable=unused-argument
from .base import LabBase, T, W

DEFAULT_THEME = {
    "foreground": "#fff",
    "background": "#000",
    "cursor": "#fff",
    "cursorAccent": "#000",
    "selection": "rgba(255, 255, 255, 0.3)",
}


@W.register
class Terminal(LabBase):
    """ A basic terminal
    """

    _model_name = T.Unicode("TerminalModel").tag(sync=True)
    _view_name = T.Unicode("TerminalView").tag(sync=True)

    rows = T.Int(24).tag(sync=True)
    cols = T.Int(80).tag(sync=True)
    selection = T.Unicode("").tag(sync=True)
    scroll = T.Int(0).tag(sync=True)
    fit = T.Bool(True).tag(sync=True)
    local_echo = T.Bool(False).tag(sync=True)
    theme = T.Dict(default_value=DEFAULT_THEME).tag(sync=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data_handlers = W.CallbackDispatcher()
        self.on_msg(self._handle_terminal_msg)

    def on_data(self, callback, remove=False):
        """ register a callback which will receive a message
        """
        self._data_handlers.register_callback(callback, remove=remove)

    def data(self, content):
        """ programatically call all data listeners
        """
        self._data_handlers(self, content)

    def send_line(self, line):
        """ convenience wrapper around send
        """
        self.send({"content": f"{line}\r\n"})

    def _handle_terminal_msg(self, _, content, buffers):
        """ handler for messages
        """
        self.data(content)
