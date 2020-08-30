""" test configuration for wxyz_notebook
"""
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
NOTEBOOKS = ROOT / "notebooks"
DESIGN = NOTEBOOKS / "Design"

NOTEBOOKS = [
    i
    for i in sorted(NOTEBOOKS.rglob("*.ipynb"))
    if "ipynb_checkpoint" not in str(i) and str(DESIGN) not in str(i)
]
