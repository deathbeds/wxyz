import sys
import shutil

import robot

from . import ATEST, ROBOT_OUT, PLATFORM


if __name__ == "__main__":
    out = ROBOT_OUT / PLATFORM

    if out.exists():
        shutil.rmtree(out)

    out.mkdir(parents=True)

    sys.exit(robot.run_cli(list(map(str, [
        "-n", "WXYZ",
        "--name",
        PLATFORM,
        "--outputdir", out,
        "--output",
        ROBOT_OUT / f"{PLATFORM}.robot.xml",
        "--log",
        ROBOT_OUT / f"{PLATFORM}.log.html",
        "--report",
        ROBOT_OUT / f"{PLATFORM}.report.html",
        "--xunit",
        ROBOT_OUT / f"{PLATFORM}.xunit.xml",
        "--variable",
        f"OS:{PLATFORM}",
        str(ATEST)
    ]))))
