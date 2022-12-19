"""source of truth for wxyz-tpl-jinja version info"""
import sys
from importlib.metadata import version
from pathlib import Path

module_name = "@deathbeds/wxyz-tpl-nunjucks"
module_version = "0.6.0"
HERE = Path(__file__).parent
SHARE = "share/jupyter/labextensions"
IN_TREE = (HERE / "../../../_d" / SHARE / module_name).resolve()
IN_PREFIX = Path(sys.prefix) / SHARE / module_name
__prefix__ = IN_TREE if IN_TREE.exists() else IN_PREFIX
NAME = "wxyz-tpl-jinja"
__version__ = version(NAME)
