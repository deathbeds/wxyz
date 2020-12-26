"""generate favicon from svg"""
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from cairosvg import svg2png
from PIL import Image

from . import _paths as P

# pixel sizes of favicons to create
SIZES = [(16, 16), (32, 32), (48, 48), (64, 64)]


def favicon():
    """generate a favicon, discarding the intermediate png (for now)"""
    with TemporaryDirectory() as td:
        tdp = Path(td)
        png = tdp / "wxyz.png"
        svg2png(bytestring=P.DOCS_LOGO.read_bytes(), write_to=str(png))
        Image.open(str(png)).save(str(P.DOCS_FAVICON), sizes=SIZES)
    return 0


if __name__ == "__main__":
    sys.exit(favicon())
