import sys

import robot

from . import ATEST, ROBOT_OUT


if __name__ == "__main__":
    sys.exit(robot.run_cli([
        "-n", "WXYZ",
        "--outputdir", str(ROBOT_OUT),
        str(ATEST)
    ]))
