from pathlib import Path
import sys

Path("env-test.yml").write_text(
    Path("env-test.in.yml").read_text().format(
        python=sys.argv[1],
        lab=sys.argv[2],
        nodejs=sys.argv[3]
    )
)
