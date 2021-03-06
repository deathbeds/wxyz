""" utilities for doit
"""
# pylint: disable=expression-not-assigned
import subprocess
from datetime import datetime

from doit.reporter import ConsoleReporter

from . import _paths as P

TIMEFMT = "%H:%M:%S"
SKIP = "        "


def call(args, **kwargs):
    """wrapper for subprocess call that handles pathlib.Path arguments (for windows)"""
    if kwargs.get("cwd"):
        kwargs["cwd"] = str(kwargs["cwd"])

    return subprocess.call([*map(str, args)], **kwargs)


def okit(name, remove=False):
    """add/remove a sentinel file"""
    ok_file = P.OK / name

    def _ok():
        if remove:
            ok_file.exists() and ok_file.unlink()
        else:
            if not ok_file.parent.exists():
                ok_file.parent.mkdir(exist_ok=True, parents=True)
            ok_file.write_text(f"{name} is ok")
        return True

    return _ok


class Reporter(ConsoleReporter):
    """a fancy reporter"""

    _timings = {}

    def execute_task(self, task):
        """start a task"""
        start = datetime.now()
        title = task.title()
        self._timings[title] = [start]
        self.outstream.write(f"""{start.strftime(TIMEFMT)} 🎢  {title}\n""")

    def outtro(self, task, emoji):
        """print out at the end of task"""
        title = task.title()
        sec = "?".rjust(7)
        if title in self._timings:
            start, end = self._timings[title] = [
                *self._timings[title],
                datetime.now(),
            ]
            delta = end - start
            sec = str(delta.seconds).rjust(7)
        self.outstream.write(f"{sec}s {emoji} {task.title()} {emoji}\n")

    def add_failure(self, task, exception):
        """special failure"""
        super().add_failure(task, exception)
        self.outtro(task, "⭕")

    def add_success(self, task):
        """special success"""
        super().add_success(task)
        self.outtro(task, "🏁 ")

    def skip_uptodate(self, task):
        """special skip"""
        self.outstream.write(f"{SKIP} ⏩  {task.title()}\n")

    skip_ignore = skip_uptodate
