"""source of truth for wxyz_json_e version info"""
import sys
from importlib.metadata import version
from pathlib import Path

module_name = "@deathbeds/wxyz-json-e"
module_version = "0.6.0"

HERE = Path(__file__).parent

IN_TREE = (HERE / f"../_d/share/jupyter/labextensions/{module_name}").resolve()
IN_PREFIX = Path(sys.prefix) / f"share/jupyter/labextensions/{module_name}"

__prefix__ = IN_TREE if IN_TREE.exists() else IN_PREFIX


NAME = "wxyz_json_e"
__version__ = version(NAME)
