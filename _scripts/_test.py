from . import IPYNB, IPYNB_HTML, PY, _run

import sys

if __name__ == "__main__":
    errors = 0

    for ipynb in sorted(IPYNB.rglob("*.ipynb")):
        if "ipynb_checkpoint" in str(ipynb):
            continue
        if sys.version_info >= (3, 8) and "importnb" in ipynb.read_bytes().decode("utf-8"):
            continue

        try:
            _run([PY, "-m",  "nbconvert", "--output-dir", IPYNB_HTML, "--execute", ipynb])
        except:
            errors += 1

    sys.exit(errors)
