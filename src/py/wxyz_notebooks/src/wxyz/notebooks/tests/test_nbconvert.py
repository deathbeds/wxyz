""" test nbconvert CLI with wxyz example notebooks
"""
import subprocess
import sys

import pytest

from .conftest import NOTEBOOKS


@pytest.mark.parametrize("name,ipynb", [[i.name, i] for i in NOTEBOOKS])
def test_notebook(name, ipynb, tmp_path):
    """ will it nbconvert?
    """
    assert (
        subprocess.call(
            [
                sys.executable,
                "-m",
                "nbconvert",
                "--output-dir",
                tmp_path,
                "--execute",
                ipynb,
            ]
        )
        == 0
    ), f"{name} failed to nbconvert --execute"
