"""source of truth for {{ project["name"] }} version info"""
{% if js_pkg %}import sys
{% endif %}from importlib.metadata import version
{% if js_pkg %}from pathlib import Path

module_name = "{{ js_pkg["name"] }}"
module_version = "{{ js_pkg["version"] }}"
HERE = Path(__file__).parent
SHARE = "share/jupyter/labextensions"
IN_TREE = (HERE / "../../../_d" / SHARE / module_name).resolve()
IN_PREFIX = Path(sys.prefix) / SHARE / module_name
__prefix__ = IN_TREE if IN_TREE.exists() else IN_PREFIX
{% endif %}NAME = "{{ project["name"] }}"
__version__ = version(NAME)
