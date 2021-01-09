""" look in setup.cfg """
# pylint: disable=invalid-name
import json
from pathlib import Path

HERE = Path(__file__).parent
__jspackage__ = json.loads(
    (HERE / "src/wxyz/notebooks/js/package.json").read_text(encoding="utf-8")
)
__version__ = __jspackage__["version"]

__import__("setuptools").setup(version=__version__)
