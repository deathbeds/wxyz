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

    if WIDGET_LOG_OUT:
        os.environ["WXYZ_WIDGET_LOG"] = str(Path(WIDGET_LOG_OUT) / f"{name}.json")

    rc = subprocess.call(
        [
            *map(
                str,
                args,
            )
        ],
    )

    os.environ.pop("WXYZ_WIDGET_LOG", None)

    assert rc == 0, f"{name} failed to nbconvert --execute"
