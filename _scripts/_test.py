import sys

from . import IPYNB, IPYNB_HTML, PY, _run

import pytest
import multiprocessing

CPU_COUNT = multiprocessing.cpu_count()

NOTEBOOKS_TO_TEST = [
    i for i in sorted(IPYNB.rglob("*.ipynb")) if "ipynb_checkpoint" not in str(i)
]

@pytest.mark.parametrize("name,ipynb", [[i.name, i] for i in NOTEBOOKS_TO_TEST])
def test_notebook(name, ipynb):
    _run([PY, "-m",  "nbconvert", "--output-dir", IPYNB_HTML, "--execute", ipynb])


if __name__ == "__main__":
    pytest.main([__file__, "-vv", "-n", str(CPU_COUNT)])
