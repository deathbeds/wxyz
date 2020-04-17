""" test configuration for wxyz_notebook
"""
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent

NOTEBOOKS = [
    i for i in sorted(ROOT.rglob("*.ipynb")) if "ipynb_checkpoint" not in str(i)
]
