""" Run acceptance tests with robot framework
"""
# pylint: disable=broad-except
import os
import shutil
import sys
import time
from os.path import join

import robot
from pabot import pabot

from . import _paths as P


def get_stem(attempt, extra_args):
    """make a directory stem with the run type, python and os version"""
    stem = "_".join([P.OS, P.PY_VER, str(attempt)]).replace(".", "_").lower()

    if "--dryrun" in extra_args:
        stem = f"dry_run_{stem}"

    return stem


def atest(attempt, extra_args):
    """perform a single attempt of the acceptance tests"""
    stem = get_stem(attempt, extra_args)

    if attempt != 1:
        previous = P.ATEST_OUT / f"{get_stem(attempt - 1, extra_args)}.robot.xml"
        if previous.exists():
            extra_args += ["--rerunfailed", str(previous)]

    if "FIREFOX_BINARY" not in os.environ:
        os.environ["FIREFOX_BINARY"] = shutil.which("firefox")

        prefix = os.environ.get("CONDA_PREFIX")

        if prefix:
            app_dir = join(prefix, "bin", "FirefoxApp")
            os.environ["FIREFOX_BINARY"] = {
                "Windows": join(prefix, "Library", "bin", "firefox.exe"),
                "Linux": join(app_dir, "firefox"),
                "Darwin": join(app_dir, "Contents", "MacOS", "firefox"),
            }[P.OS]

    print("Will use firefox at", os.environ["FIREFOX_BINARY"])

    assert os.path.exists(
        os.environ["FIREFOX_BINARY"]
    ), "No firefox found, this would not go well"

    out_dir = P.ATEST_OUT / stem

    args = [
        "--name",
        f"{P.OS}{P.PY_VER}",
        "--outputdir",
        out_dir,
        "--log",
        out_dir / "log.html",
        "--report",
        out_dir / "report.html",
        "--xunit",
        out_dir / "xunit.xml",
        "--variable",
        f"OS:{P.OS}",
        "--variable",
        f"PY:{P.PY_VER}",
        "--variable",
        f"WXYZ_NOTEBOOKS:{P.IPYNB}",
        "--randomize",
        "all",
        *(extra_args or []),
    ]

    os.chdir(P.ATEST)

    if out_dir.exists():
        print(f"trying to clean out {out_dir}")
        try:
            shutil.rmtree(out_dir)
        except Exception as err:
            print(f"Error deleting {out_dir}, hopefully harmless: {err}")

    if "--dryrun" in extra_args:
        run_robot = robot.run_cli
        fake_cmd = "robot"
    else:
        run_robot = pabot.main
        fake_cmd = "pabot"
        # pabot args must come first
        args = [
            "--artifactsinsubfolders",
            "--artifacts",
            "png,log",
            "--testlevelsplit",
            *args,
        ]

    print(f"[{fake_cmd} arguments]\n", " ".join(list(map(str, args))))
    print(f"[{fake_cmd} test root]\n", P.ATEST)

    try:
        run_robot(list(map(str, args + [P.ATEST])))
        return 0
    except SystemExit as err:
        print(run_robot.__name__, "exited with", err.code)
        return err.code


def attempt_atest_with_retries(*extra_args):
    """retry the robot tests a number of times"""
    attempt = 0
    error_count = -1

    retries = int(os.environ.get("ATEST_RETRIES") or "0")

    while error_count != 0 and attempt <= retries:
        attempt += 1
        print(f"attempt {attempt} of {retries + 1}...")
        start_time = time.time()
        error_count = atest(attempt=attempt, extra_args=list(extra_args))
        print(error_count, "errors in", int(time.time() - start_time), "seconds")

    return error_count


if __name__ == "__main__":
    sys.exit(attempt_atest_with_retries(*sys.argv[1:]))
