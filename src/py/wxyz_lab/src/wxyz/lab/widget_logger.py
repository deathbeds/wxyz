import IPython.core.ultratb
import ipywidgets as W
import logging
import queue
import re
import traitlets as T

from pygments import highlight
from pygments.formatters import TerminalTrueColorFormatter
from pygments.style import Style
from pygments.token import Comment, Name, Generic, String

from .widget_term import Terminal


class XStream(W.Widget):
    terminal = T.Instance(Terminal, kw={})
    """Stream Widget that points to an keeps an internal queue or msgs until the there is an 
    active xtermjs terminal.
    """
     
    def write(self, msg):
        msg = msg.strip("\n").replace("\n","\n\r")
        if not msg:
            return

        self.terminal.send_line(msg)


class DarkLogStyle(Style):
    """Default Log Style for dark backgrounds"""
    styles = {
        Comment:            "italic ansiyellow",

        Name.Namespace:     "ansimagenta",  # logger name
        Name.Tag:           "ansigreen",  # logger time
        Name.Decorator:     "italic ansicyan",  # logger level name
        
        Generic.Inserted:   "ansibrightgreen",  # logging.DEBUG
        Generic.Output:     "ansibrightcyan",  # logging.INFO
        Generic.Prompt:     "bold ansibrightyellow",  # logging.WARN
        Generic.Error:      "ansibrightred",  # logging.ERROR
        Generic.Strong:     "bold ansibrightred",  # logging.CRITICAL
        
        String.Delimiter:   "ansiwhite",  # misc formatter characters
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
            "levelname": Name.Decorator,
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