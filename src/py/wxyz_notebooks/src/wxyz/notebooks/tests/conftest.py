""" test configuration for wxyz_notebook
"""
import platform
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
NOTEBOOKS = ROOT / "notebooks"
EXAMPLES = NOTEBOOKS / "examples"
DESIGN = NOTEBOOKS / "Design"
OS = platform.system()

OS_SKIP = {"Windows": [EXAMPLES / "TPOTWXYZ.ipynb", EXAMPLES / "SKWXYZ.ipynb"]}

TEST_NOTEBOOKS = [
    ipynb
    for ipynb in sorted(NOTEBOOKS.rglob("*.ipynb"))
    if (
        "ipynb_checkpoint" not in str(ipynb)
        and str(DESIGN) not in str(ipynb)
        and ipynb not in OS_SKIP.get(OS, [])
    )
]
