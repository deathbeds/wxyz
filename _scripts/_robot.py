import sys
import shutil
import os
import robot

from . import ATEST, ROBOT_OUT, PLATFORM, ROOT


if __name__ == "__main__":
    # TODO: matrix this
    browser = "headlessfirefox"

    out = ROBOT_OUT / f"{browser}_{PLATFORM}"

    if out.exists():
        shutil.rmtree(out)

    out.mkdir(parents=True)

    os.environ["PROJECT_DIR"] = str(ROOT)

    sys.exit(robot.run_cli(list(map(str, [
        "-n", "WXYZ",
        "--name",
        f"{browser}_{PLATFORM}",
        "--outputdir", out,
        "--output",
        ROBOT_OUT / f"{browser}_{PLATFORM}.robot.xml",
        "--log",
        ROBOT_OUT / f"{browser}_{PLATFORM}.log.html",
        "--report",
        ROBOT_OUT / f"{browser}_{PLATFORM}.report.html",
        "--xunit",
        ROBOT_OUT / f"{browser}_{PLATFORM}.xunit.xml",
        "--variable",
        f"OS:{PLATFORM}",
        "--variable",
        f"BROWSER:{browser}",
        str(ATEST)
    ]))))
