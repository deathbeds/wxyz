""" utilities for doit
"""
import subprocess


def call(args, **kwargs):
    """ wrapper for subprocess call that handles pathlib.Path arguments (for windows)
    """
    if kwargs.get("cwd"):
        kwargs["cwd"] = str(kwargs["cwd"])

    return subprocess.call([*map(str, args)], **kwargs)
