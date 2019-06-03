from . import IPYNB, IPYNB_HTML, PY, _run

if __name__ == "__main__":
    for ipynb in IPYNB.rglob("*.ipynb"):
        if "ipynb_checkpoint" in str(ipynb):
            continue
        _run([PY, "-m",  "nbconvert", "--output-dir", IPYNB_HTML, "--execute", ipynb])
