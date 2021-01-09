""" test configuration for wxyz_notebook
"""
# pylint: disable=fixme
import os
import platform
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
NOTEBOOKS = ROOT / "notebooks"
EXAMPLES = NOTEBOOKS / "examples"
DESIGN = NOTEBOOKS / "Design"
OS = platform.system()

WIDGET_LOG_OUT = os.environ.get("WXYZ_WIDGET_LOG_OUT")

OS_SKIP = {
    # TODO: remove
    # previously couldn't run these example on windows
    # "Windows": [EXAMPLES / "TPOTWXYZ.ipynb"]
}

# Names of just-don't-run these tests
ALL_SKIP = os.environ.get("WXYZ_SKIP_NOTEBOOK", "").split(" ")

TEST_NOTEBOOKS = [
    ipynb
    for ipynb in sorted(NOTEBOOKS.rglob("*.ipynb"))
    if (
        "ipynb_checkpoint" not in str(ipynb)
        and str(DESIGN) not in str(ipynb)
        and ipynb not in OS_SKIP.get(OS, [])
        and ipynb.name not in ALL_SKIP
    )
]
