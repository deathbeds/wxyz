""" test nbconvert CLI with wxyz example notebooks
"""
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from .conftest import TEST_NOTEBOOKS, WIDGET_LOG_OUT


@pytest.mark.parametrize("name,ipynb", [[i.stem, i] for i in TEST_NOTEBOOKS])
def test_notebook(name, ipynb, tmp_path):
    """will it nbconvert?"""
    retries = 3
    attempt = 0
    rc = 1
    while attempt < retries:
        rc = _attempt_one(name, ipynb, tmp_path)
        if rc == 0:
            break
        attempt += 1
        time.sleep(attempt * 3)

    assert rc == 0, f"kept failing after {attempt} attempts"


def _attempt_one(name, ipynb, tmp_path):
    args = [
        sys.executable,
        "-m",
        "nbconvert",
        "--to",
        "html",
        "--ExecutePreprocessor.timeout=600",
        "--output-dir",
        tmp_path,
        "--execute",
        ipynb,
    ]

    env = dict(os.environ)

    work_path = tmp_path / "_wxyz_work"
    env["WXYZ_TEST_WORK_DIR"] = str(work_path)

    if WIDGET_LOG_OUT:
        env["WXYZ_WIDGET_LOG"] = str(Path(WIDGET_LOG_OUT) / f"{name}.json")

    rc = subprocess.call([*map(str, args)], env=env)

    os.environ.pop("WXYZ_WIDGET_LOG", None)

    return rc
