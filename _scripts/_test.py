from . import IPYNB, IPYNB_HTML, PY, _run

import sys

if __name__ == "__main__":
    for ipynb in IPYNB.rglob("*.ipynb"):
        if "ipynb_checkpoint" in str(ipynb):
            continue
        if sys.version_info >= (3, 8) and "importnb" in ipynb.read_text():
            continue
        _run([PY, "-m",  "nbconvert", "--output-dir", IPYNB_HTML, "--execute", ipynb])
