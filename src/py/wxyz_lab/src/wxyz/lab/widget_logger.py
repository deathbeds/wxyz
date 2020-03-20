import IPython.core.ultratb
import ipywidgets as W
import logging
import queue
import re
import traitlets as T

from pygments import highlight
from pygments.formatters import HtmlFormatter, TerminalTrueColorFormatter
from pygments.style import Style
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation, Generic, Other, Error, Whitespace

from .widget_term import Terminal


class XStream(W.Widget):
    terminal = T.Instance(Terminal, kw={})
    io: queue.Queue
    def __init__(self, maxsize=None, *args, **kwargs):
        """Stream Widget that keeps an internal queue or msgs until the there is an 
        active xtermjs terminal.
        """
        super().__init__(*args, **kwargs)
        self.maxsize = maxsize
        self._changed_terminal()

    @T.observe("terminal")
    def _changed_terminal(self, change:T.Bunch=None):
        if change and isinstance(change.old, Terminal):
            change.old.unobserve(self._connected, "active_terminals")
        
        if not self.terminal.active_terminals:
            self.terminal.observe(self._connected, "active_terminals")
            self.io = queue.Queue(maxsize=self.maxsize)
        else:
            self._connected()

    def _connected(self, change):
        self.terminal.unobserve(self._connected, "active_terminals")
        if self.io is None:
            # no messages to flush
            return
        while True:
            try:
                msg = self.io.get_nowait()
                self._fl = msg
                self.terminal.send_line(msg)
            except queue.Empty:
                break        
        self.io = None        

    def write(self, msg):
        msg = msg.strip("\n").replace("\n","\n\r")
        if not msg:
            return
        
        if self.io is not None:
            # put message in queue
            try:
                self.io.put_nowait(msg)
            except queue.Full:
                drop_msg = self.io.get_nowait()
                self.io.put_nowait(msg)
        else:
            # broadcast message to terminal
            self.terminal.send_line(msg)


class DarkLogStyle(Style):
    """Default Log Style for dark backgrounds"""

    background_color = "#f8f8f8"
    default_style = ""

    styles = {
        Comment:                   "italic #408080",

        Name.Namespace:            "#5050d6",
        Name.Tag:                  "#008000",
        Name.Decorator:            "#AA22FF",
        
        Generic.Inserted:          "#00A000",
        Generic.Error:             "#FF0000",
        Generic.Emph:              "italic",
        Generic.Strong:            "bold #FF0000",
        Generic.Prompt:            "bold #ffda4c",
        Generic.Output:            "#cccccc",
        Generic.Traceback:         "#04D",
        
        String.Delimiter:          "",
        
        Error:                     "border:#FF0000"
    }            


class PythonLoggingRecordLexer(object):
    """
    A lexer for records generated with python logging module
    """
    def __init__(self, fmt:str):
        pattern = re.compile("%\((\w*)\)s([^%]*)")
        self.log_fmt = list(re.findall(pattern, fmt))
        self.token_map = {
            "name": Name.Namespace,
            "asctime": Name.Tag,
            logging.DEBUG: Generic.Inserted,
            logging.INFO: Generic.Output,
            logging.WARN: Generic.Prompt,
            logging.ERROR: Generic.Error,
            logging.CRITICAL: Generic.Strong,
        }
        
    def get_tokens(self, record):
        """Build the pygment tokens for the record based on the given log format sequence"""
        
        for key, delimeter in self.log_fmt:
            attr = getattr(record, key, None)
            token = Comment
            if key == "message":
                token = self.token_map.get(record.levelno)
            else:
                token = self.token_map.get(key, Comment)
            yield (token, f"{attr}")
            yield (String.Delimiter, f"{delimeter}")


class ColoredFormatter(logging.Formatter):
    def __init__(self, style=DarkLogStyle, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._lexer = PythonLoggingRecordLexer(fmt=self._fmt)
        self._formatter = TerminalTrueColorFormatter(style=style)
    
    def formatMessage(self, record):
        return highlight(record, self._lexer, self._formatter)
    
    def formatException(self, exc_info):
        """Apply IPython colors to system exception info"""
        tb = IPython.core.ultratb.VerboseTB()
        return tb.text(*exc_info)
    
    def formatStack(self, stack_info):
        """Apply IPython colors to system exception info"""
        return super().formatStack(stack_info)


if __name__ == "__main__":
    stream = XStream()

    logger = logging.getLogger()
    handler = logging.StreamHandler(stream=stream)
    colorer = ColoredFormatter(
        fmt="%(asctime)s-%(name)s:%(levelname)s- %(message)s",
        datefmt='%H:%M:%S',
    )
    logger.setLevel(logging.DEBUG)
    handler.setFormatter(colorer)
    logger.addHandler(handler)

    stream.terminal