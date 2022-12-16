"""source of truth for wxyz_html version info"""
import sys
from importlib.metadata import version
from pathlib import Path

module_name = "@deathbeds/wxyz-html"
module_version = "0.6.0"

HERE = Path(__file__).parent

SHARE = "share/jupyter/labextensions"
IN_TREE = (HERE / "../../../_d" / SHARE / module_name).resolve()
IN_PREFIX = Path(sys.prefix) / SHARE / module_name

__prefix__ = IN_TREE if IN_TREE.exists() else IN_PREFIX


NAME = "wxyz_html"
__version__ = version(NAME)
