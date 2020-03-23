""" Terminal viewing widgets
"""
# pylint: disable=unused-argument,no-name-in-module,import-error
import re
import queue

from ipywidgets import trait_types

from .base import LabBase, T, W

DEFAULT_THEME = {
    "foreground": "#fff",
    "background": "#000",
    "cursor": "#fff",
    "cursorAccent": "#000",
    "selection": "rgba(255, 255, 255, 0.3)",
}

# this is copied from xterm.d.ts
DTS = (
    """
    /**
     * Retrieves an option's value from the terminal.
     * @param key The option key.
     */
    getOption(key: 'bellSound' | 'bellStyle' | 'cursorStyle' | 'fontFamily'"""
    """ | 'fontWeight' | 'fontWeightBold'| 'rendererType' | 'termName'): string;
    /**
     * Retrieves an option's value from the terminal.
     * @param key The option key.
     */
    getOption(key: 'allowTransparency' | 'cancelEvents' | 'convertEol'"""
    """ | 'cursorBlink' | 'debug' | 'disableStdin' | 'enableBold' | """
    """ | 'macOptionIsMeta' | 'rightClickSelectsWord' | 'popOnBell' | 'screenKeys'"""
    """ | 'useFlowControl' | 'visualBell'): boolean; """
    """
/**
     * Retrieves an option's value from the terminal.
     * @param key The option key.
     */
    getOption(key: 'colors'): string[];
    /**
     * Retrieves an option's value from the terminal.
     * @param key The option key.
     */
    getOption(key: 'cols' | 'fontSize' | 'letterSpacing' | 'lineHeight'"""
    """ | 'rows' | 'tabStopWidth' | 'scrollback'): number;
"""
)

TRAIT_MAP = {
    "number": T.Float,
    "boolean": T.Bool,
    "string[]": lambda **kwargs: trait_types.TypedTuple(T.Unicode(), **kwargs),
    "string": T.Unicode,
}


def _traits_from_dts():
    traits = {}
    for attrs, dts_type in re.findall(r"getOption\(key: (.*)\): (.*);", DTS):
        for attr in re.findall(r"'(.*?)'", attrs):
            if attr in ["rows", "cols"]:
                continue
            traits[re.sub(r"(?<!^)(?=[A-Z])", "_", attr).lower()] = TRAIT_MAP[dts_type](
                default_value=None, allow_none=True
            ).tag(sync=True)
    return traits


@W.register
class Terminal(LabBase):
    """ A basic terminal
    """

    _model_name = T.Unicode("TerminalModel").tag(sync=True)
    _view_name = T.Unicode("TerminalView").tag(sync=True)

    locals().update(_traits_from_dts())

    rows = T.Int(24).tag(sync=True)
    cols = T.Int(80).tag(sync=True)
    selection = T.Unicode("").tag(sync=True)
    scroll = T.Int(0).tag(sync=True)
    fit = T.Bool(True).tag(sync=True)
    local_echo = T.Bool(False).tag(sync=True)
    theme = T.Dict(default_value=DEFAULT_THEME).tag(sync=True)
    active_terminals = T.Int(0).tag(sync=True)
    buffer = T.Instance(queue.Queue)
    buffer_size = T.Int(allow_none=True)

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
        if self.active_terminals >= 1:
            self.send({"content": f"{line}\r\n"})
        else:
            self._buffer_message(line)

    def _handle_terminal_msg(self, _, content, buffers):
        """ handler for messages
        """
        self.data(content)
    
    def _buffer_message(self, msg):
        """Add message to the buffer by potentially dropping the oldest"""
        try:
            self.buffer.put_nowait(msg)
        except queue.Full:
            drop_msg = self.buffer.get_nowait()
            self.buffer.put_nowait(msg)

    @T.observe("active_terminals")
    def _flush(self, change=None):
        """Flush buffer queue to the terminal"""
        while self.active_terminals > 0:
            try:
                msg = self.buffer.get_nowait()
                self.send_line(msg)
            except queue.Empty:
                break

    @T.default("buffer")
    def _default_buffer(self):
        return queue.Queue(maxsize=self.buffer_size)

    @T.observe("buffer_size")
    def _change_buffer_size(self, change):
        buffer = self.buffer
        current_size = buffer.qsize()
        if current_size > self.buffer_size:
            for i in range(current_size-self.buffer_size):
                drop_msg = buffer.get_nowait()
        buffer.maxsize = self.buffer_size


