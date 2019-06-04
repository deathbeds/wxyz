from . import ROBOT_OUT, _run


def combine():
    args = [
        "python",
        "-m",
        "robot.rebot",
        "--name",
        "WXYZ",
        "--outputdir",
        ROBOT_OUT,
        "--output",
        "output.xml",
    ] + list(map(str, ROBOT_OUT.glob("*.robot.xml")))

    return _run(args)


if __name__ == "__main__":
    combine()
