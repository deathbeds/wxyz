"""generated setup for wxyz_core, do not edit by hand"""
import json
from pathlib import Path

WXYZ_NAME = "core"

HERE = Path(__file__).parent
JS_PKG = HERE / f"src/wxyz/{WXYZ_NAME}/js/package.json"

__jspackage__ = json.loads(JS_PKG.read_text(encoding="utf-8"))


HERE = Path(__file__).parent
EXT_NAME = __jspackage__["name"]

EXT_FILES = {}

SHARE = f"share/jupyter/labextensions/{EXT_NAME}"

EXT = HERE / f"src/wxyz/{WXYZ_NAME}/labextension"

for ext_path in [EXT] + [d for d in EXT.rglob("*") if d.is_dir()]:
    if ext_path == EXT:
        target = str(SHARE)
    else:
        target = f"{SHARE}/{ext_path.relative_to(EXT)}"
    EXT_FILES[target] = [
        str(p.relative_to(HERE).as_posix())
        for p in ext_path.glob("*")
        if not p.is_dir()
    ]

ALL_FILES = sum(EXT_FILES.values(), [])

assert (
    len([p for p in ALL_FILES if "remoteEntry" in str(p)]) == 1
), "expected _exactly one_ remoteEntry.*.js"

EXT_FILES[SHARE] += [f"src/wxyz/{WXYZ_NAME}/install.json"]

SETUP_ARGS = dict(
    version=__jspackage__["version"],
    data_files=[(str(k), list(map(str, v))) for k, v in EXT_FILES.items()],
)

if __name__ == "__main__":
    import setuptools

    setuptools.setup(**SETUP_ARGS)
