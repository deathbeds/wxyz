""" utilities for doit
"""
# pylint: disable=expression-not-assigned
import email.utils
import json
import os
import re
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


def template_one(src: Path, dest: Path, context):
    """template something."""
    jinja2 = __import__("jinja2")
    tmpl_src = src.read_text(encoding="utf-8")
    tmpl = jinja2.Template(tmpl_src)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(tmpl.render(**context), encoding="utf-8")


def typedoc_conf():
    """generate typedoc configuration"""
    typedoc = json.loads(P.TYPEDOC_JSON.read_text(encoding="utf-8"))
    original_entry_points = sorted(typedoc["entryPoints"])
    new_entry_points = sorted(
        [
            f"packages/{pkg.parent.name}"
            for pkg in P.TS_PACKAGE
            if pkg.parent.name not in P.NO_TYPEDOC
        ]
    )

    if json.dumps(original_entry_points) != json.dumps(new_entry_points):
        typedoc["entryPoints"] = new_entry_points
        P.TYPEDOC_JSON.write_text(
            json.dumps(typedoc, indent=2, sort_keys=True), encoding="utf-8"
        )

    tsconfig = json.loads(P.TSCONFIG_TYPEDOC.read_text(encoding="utf-8"))
    original_references = tsconfig["references"]
    new_references = [
        {"path": f"./packages/{pkg.parent.name}"}
        for pkg in sorted(P.TS_PACKAGE)
        if pkg.parent.name not in P.NO_TYPEDOC
    ]

    if json.dumps(original_references) != json.dumps(new_references):
        tsconfig["references"] = new_references
        P.TSCONFIG_TYPEDOC.write_text(
            json.dumps(tsconfig, indent=2, sort_keys=True), encoding="utf-8"
        )


def mystify():
    """unwrap monorepo docs into per-module docs"""
    if P.DOCS_JS.exists():
        shutil.rmtree(P.DOCS_JS)

    def unescape_name_header(matchobj):
        unescaped = matchobj.group(1).replace("\\_", "_")
        if unescaped not in ["Interfaces"]:
            unescaped = f"`{unescaped}`"
        return f"""### {unescaped}"""

    def unescape_bold(matchobj):
        unescaped = matchobj.group(1).replace("\\_", "_")
        return f"""**`{unescaped}`**"""

    for doc in sorted(P.DOCS_RAW_TYPEDOC.rglob("*.md")):
        if doc.parent == P.DOCS_RAW_TYPEDOC:
            continue
        if doc.name == "README.md":
            continue
        doc_text = doc.read_text(encoding="utf-8")
        doc_lines = doc_text.splitlines()

        # rewrite doc and write back out
        out_doc = P.DOCS_JS / doc.relative_to(P.DOCS_RAW_TYPEDOC)
        if not out_doc.parent.exists():
            out_doc.parent.mkdir(parents=True)

        out_text = "\n".join([*doc_lines[1:], ""]).replace("README.md", "index.md")
        out_text = re.sub(
            r"## Table of contents(.*?)\n## ",
            "\n## ",
            out_text,
            flags=re.M | re.S,
        )
        out_text = re.sub(r"^# Module: (.*)$", r"# `\1`", out_text, flags=re.M)
        out_text = re.sub(r"^# (.*): (.*)$", r"# \1: `\2`", out_text, flags=re.M)
        out_text = re.sub(r"^### (.*)$", unescape_name_header, out_text, flags=re.M)
        out_text = re.sub(r"^[\-_]{3}$", "", out_text, flags=re.M)
        # what even is this
        out_text = re.sub(r"^[•▸] ", ">\n> ", out_text, flags=re.M)
        out_text = re.sub(r"\*\*([^\*]+)\*\*", unescape_bold, out_text, flags=re.M)
        out_text = out_text.replace("/src]", "]")
        out_text = re.sub(r"/src$", "", out_text, flags=re.M)
        out_text = re.sub(
            r"^((Implementation of|Overrides|Inherited from):)",
            "_\\1_",
            out_text,
            flags=re.M | re.S,
        )
        out_text = re.sub(
            r"^Defined in: ([^\n]+)$",
            "_Defined in:_ `\\1`",
            out_text,
            flags=re.M | re.S,
        )

        out_doc.write_text(out_text, encoding="utf-8")

    for index in [
        P.DOCS_JS_MYST_INTERFACES,
        P.DOCS_JS_MYST_MODULES,
        P.DOCS_JS_MYST_CLASSES,
    ]:
        name = index.name[:-3]
        index.write_text(
            "\n".join(
                [
                    f"# {name.title()}",
                    "\n",
                    "```{toctree}",
                    ":maxdepth: 1",
                    ":glob:",
                    f"{name}/*",
                    "```",
                ]
            )
        )

    P.DOCS_JS_MYST_INDEX.write_text(
        "\n".join(
            [
                "# `@deathbeds`\n",
                "```{toctree}",
                ":maxdepth: 1",
                "modules",
                "interfaces",
                "classes",
                "```",
            ]
        ),
        encoding="utf-8",
    )


def sort_unique_file(path: Path):
    """sort the unique lines of a file.

    sorts by lowercase, then by the case of the first letter, which seems reasonable
    """
    text = path.read_text(encoding="utf-8")
    lines = [line.strip() for line in text.strip().splitlines()]
    lines = sorted(set(lines), key=lambda x: (x.upper(), x[0] != x[0].lower()))
    new_text = "\n".join([*lines, ""])
    path.write_text(new_text, encoding="utf-8")
