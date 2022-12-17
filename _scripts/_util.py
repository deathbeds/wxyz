""" utilities for doit
"""
# pylint: disable=expression-not-assigned
import email.utils
import os
import shutil
import subprocess
import tempfile
import time
import urllib.request
from datetime import datetime
from pathlib import Path

from doit.reporter import ConsoleReporter

from . import _paths as P

TIMEFMT = "%H:%M:%S"
SKIP = "        "


def call(args, **kwargs):
    """wrapper for subprocess call that handles pathlib.Path arguments (for windows)"""
    if kwargs.get("cwd"):
        kwargs["cwd"] = str(kwargs["cwd"])

    return subprocess.call([*map(str, args)], **kwargs) == 0


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


def copy_one(src, dest):
    """copy a file (ensuring parents)"""
    if dest.is_dir():
        shutil.rmtree(dest)
    elif dest.exists():
        dest.unlink()

    if not dest.parent.exists():
        dest.parent.mkdir(parents=True)

    if src.is_dir():
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest)


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

    def add_failure(self, task, fail):
        """special failure"""
        super().add_failure(task, fail)
        self.outtro(task, "⭕")

    def add_success(self, task):
        """special success"""
        super().add_success(task)
        self.outtro(task, "🏁 ")

    def skip_uptodate(self, task):
        """special skip"""
        self.outstream.write(f"{SKIP} ⏩  {task.title()}\n")

    skip_ignore = skip_uptodate


def fetch_one(url, dest):
    """fetch one file"""

    if dest.exists():
        print(f"    - already downloaded {dest.name}, skipping...")
        return

    if not dest.parent.exists():
        dest.parent.mkdir(parents=True)

    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        with urllib.request.urlopen(url) as response:
            tmp_dest = tdp / dest.name
            with tmp_dest.open("wb") as fd:
                shutil.copyfileobj(response, fd)
            last_modified = response.headers.get("Last-Modified")
            if last_modified:
                epoch_time = time.mktime(email.utils.parsedate(last_modified))
                os.utime(tmp_dest, (epoch_time, epoch_time))
        shutil.copy2(tmp_dest, dest)


def extract_one(archive: Path, dest: Path):
    """extract the contents of an archive to a path."""
    if dest.exists():
        shutil.rmtree(dest)

    dest.mkdir(parents=True)

    old_cwd = os.getcwd()
    os.chdir(str(dest))
    try:
        __import__("libarchive").extract_file(str(archive))
    finally:
        os.chdir(old_cwd)
