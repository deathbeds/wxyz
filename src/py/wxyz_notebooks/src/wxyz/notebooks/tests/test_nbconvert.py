""" test nbconvert CLI with wxyz example notebooks
"""
import os
import subprocess
import sys
from pathlib import Path

import pytest

from .conftest import TEST_NOTEBOOKS, WIDGET_LOG_OUT


@pytest.mark.parametrize("name,ipynb", [[i.stem, i] for i in TEST_NOTEBOOKS])
def test_notebook(name, ipynb, tmp_path):
    """will it nbconvert?"""
    args = [
        sys.executable,
        "-m",
        "nbconvert",
        "--to",
        "html",
        "--output-dir",
        tmp_path,
        "--execute",
        ipynb,
    ]

    env = dict(os.environ)
    if WIDGET_LOG_OUT:
        env["WXYZ_WIDGET_LOG"] = Path(WIDGET_LOG_OUT) / f"{ipynb.name}.json"

    assert (
        subprocess.call(
            [
                *map(
                    str,
                    args,
                )
            ]
        )
        == 0
    ), f"{name} failed to nbconvert --execute"
