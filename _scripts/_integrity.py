""" integrity checks for the wxyz repo
"""

# pylint: disable=redefined-outer-name
import sys
import tempfile
from pathlib import Path

import pytest

PYTEST_INI = """
[pytest]
junit_family = xunit2
"""

sys.path += [Path(__file__).parent]
P = __import__("_paths")


@pytest.fixture(scope="module")
def contributing_text():
    """the text of CONTRIBUTING.md"""
    return P.CONTRIBUTING.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def readme_text():
    """the text of README.md"""
    return P.README.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def postbuild():
    """the text of postBuild"""
    return P.POSTBUILD.read_text(encoding="utf-8")


def test_contributing_locks(contributing_text):
    """do lockfiles mentioned exist?"""
    found_lock = 0

    for lock in P.LOCKS.glob("*"):
        if str(lock.relative_to(P.ROOT).as_posix()) in contributing_text:
            found_lock += 1

    assert found_lock == 2


def test_binder_locks(postbuild):
    """is the binder lock right?"""
    for lock in P.LOCKS.glob("conda.binder.*.lock"):
        lock_path = str(lock.relative_to(P.ROOT).as_posix())
        assert lock_path in postbuild


@pytest.mark.parametrize(
    "pkg",
    [setup_py.parent.name for setup_py in P.PY_VERSION],
)
def test_readme_py_pkgs(pkg, readme_text):
    """Are all of the python packages mentioned in the readme?"""
    assert pkg in readme_text


def check_integrity():
    """actually run the tests"""
    args = ["-vv", "-o", f"junit_suite_name=integrity_{P.OS}_{P.PY_VER}", __file__]

    with tempfile.TemporaryDirectory() as tmp:
        ini = Path(tmp) / "pytest.ini"
        ini.write_text(PYTEST_INI)

        args += ["-c", str(ini)]

        return pytest.main(args)


if __name__ == "__main__":
    sys.exit(check_integrity())
