""" utilities for doit
"""
# pylint: disable=expression-not-assigned
import subprocess

from . import _paths as P


def call(args, **kwargs):
    """ wrapper for subprocess call that handles pathlib.Path arguments (for windows)
    """
    if kwargs.get("cwd"):
        kwargs["cwd"] = str(kwargs["cwd"])

    return subprocess.call([*map(str, args)], **kwargs)


def okit(name, remove=False):
    """ add/remove a sentinel file
    """
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
