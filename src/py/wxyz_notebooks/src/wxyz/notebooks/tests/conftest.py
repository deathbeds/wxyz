from pathlib import Path

import pytest

HERE = Path(__file__).parent
ROOT = HERE.parent.parent

NOTEBOOKS = [
    i for i in sorted(ROOT.rglob("*.ipynb"))
    if "ipynb_checkpoint" not in str(i)
]
