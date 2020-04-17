import sys
import pytest
import subprocess

from .conftest import NOTEBOOKS


@pytest.mark.parametrize("name,ipynb", [[i.name, i] for i in NOTEBOOKS])
def test_notebook(name, ipynb, tmp_path):
    subprocess.check_call([
        sys.executable, "-m",  "nbconvert", "--output-dir", tmp_path, "--execute", ipynb
    ])
