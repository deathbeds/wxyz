""" integrity checks for the wxyz repo
"""
# pylint: disable=redefined-outer-name
import sys
import tempfile
from importlib.util import find_spec
from pathlib import Path

import pytest

from . import _paths as P

PYTEST_INI = """
[pytest]
junit_family=xunit2
"""


@pytest.fixture(scope="module")
def contributing_text():
    """the text of CONTRIBUTING.md"""
    return P.CONTRIBUTING.read_text(encoding="utf-8")


def test_contributing_locks(contributing_text):
    """do lockfiles mentioned exist?"""
    found_lock = 0

    for lock in P.LOCKS.glob("*"):
        if str(lock.relative_to(P.ROOT).as_posix()) in contributing_text:
            found_lock += 1

    assert found_lock == 2


@pytest.mark.parametrize(
    "pkg,version",
    [[setup_py.parent.name, version] for setup_py, version in P.PY_VERSION.items()],
)
def test_py_versions(pkg, version):
    """are version files consistent?"""
    setup_cfg = (P.PY_SRC / pkg / "setup.cfg").read_text()

    assert f"version = {version}" in setup_cfg

    if "notebooks" not in pkg:
        recipe = (P.RECIPES / pkg.replace("_", "-") / "meta.yaml").read_text()

        assert f"""{{% set version = "{version}" %}}""" in recipe


def check_integrity():
    """actually run the tests"""
    args = ["-vv", __file__]

    try:
        if find_spec("pytest_azurepipelines"):
            args += ["--no-coverage-upload"]
    except ImportError:
        pass

    with tempfile.TemporaryDirectory() as tmp:
        ini = Path(tmp) / "pytest.ini"
        ini.write_text(PYTEST_INI)

        args += ["-c", str(ini)]

        return pytest.main(args)


if __name__ == "__main__":
    sys.exit(check_integrity())
