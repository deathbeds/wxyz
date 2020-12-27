""" integrity checks for the wxyz repo
"""
import re

# pylint: disable=redefined-outer-name
import sys
import tempfile
from importlib.util import find_spec
from pathlib import Path

import pytest

from . import _paths as P

PYTEST_INI = """
[pytest]
junit_family = xunit2
"""


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


@pytest.fixture(scope="module")
def wxyz_notebook_cfg():
    """the notebook setup.cfg"""
    pys = [pys for pys in P.PY_SETUP if pys.parent.name == "wxyz_notebooks"][0]
    return (pys.parent / "setup.cfg").read_text(encoding="utf-8")


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


@pytest.mark.parametrize(
    "pkg",
    [P.TS_PACKAGE_CONTENT[p / "package.json"]["name"] for p in P.WXYZ_LAB_EXTENSIONS],
)
def test_readme_labext(pkg, readme_text):
    """Are all of the labextensions mentioned in the readme?"""
    assert pkg in readme_text


@pytest.mark.parametrize(
    "pkg,version",
    [[setup_py.parent.name, version] for setup_py, version in P.PY_VERSION.items()],
)
def test_py_versions(pkg, version):
    """are version files consistent?"""
    setup_cfg = (P.PY_SRC / pkg / "setup.cfg").read_text(encoding="utf-8")

    assert f"version = {version}" in setup_cfg


@pytest.mark.parametrize(
    "pkg_name,pkg_path",
    [[setup_py.parent.name, setup_py.parent] for setup_py in P.PY_VERSION],
)
def test_manifest(pkg_name, pkg_path):
    """are manifest files proper?"""
    manifest = pkg_path / "MANIFEST.in"
    manifest_txt = manifest.read_text(encoding="utf-8")

    assert re.findall(
        r"include .*LICENSE.txt", manifest_txt
    ), f"{pkg_name} missing license in {manifest}"
    assert re.findall(
        r"global-exclude\s+.ipynb_checkpoints", manifest_txt
    ), f"{pkg_name} missing checkpoint exclude in {manifest}"


@pytest.mark.parametrize("pkg_path", P.PY_SETUP)
def test_notebook_deps(wxyz_notebook_cfg, pkg_path):
    """does the notebook example package depend on all other packages?"""
    pkg = pkg_path.parent.name
    assert pkg in wxyz_notebook_cfg, f"add {pkg} to wxyz_notebook/setup.cfg!"


def check_integrity():
    """actually run the tests"""
    args = ["-vv", "-o", f"junit_suite_name=integrity_{P.OS}_{P.PY_VER}", __file__]

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
