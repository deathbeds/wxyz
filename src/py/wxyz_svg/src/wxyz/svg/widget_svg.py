""" SVG Box widget
"""
# pylint: disable=unused-argument
from pathlib import Path

from .base import SVGBase, T, W

# default XML attribute, with an Inkscape default
DEFAULT_ATTR = "inkscape:label"


@W.register
class SVGBox(SVGBase, W.Box):
    """An SVG Box that shows its children inside the bounding box of
    named areas in an SVG file.

    """

    _model_name = T.Unicode("SVGBoxModel").tag(sync=True)
    _view_name = T.Unicode("SVGBoxView").tag(sync=True)

    # unsynced trait
    svg_file = T.Unicode(help="a path to local .svg file")

    svg = T.Unicode(help="an SVG string").tag(sync=True)
    show_svg = T.Bool(True, help="only use SVG for sizing, do no show").tag(sync=True)
    area_attr = T.Unicode(
        DEFAULT_ATTR, help="namespaced XML attribute on SVG `g`s " "with unique values"
    ).tag(sync=True)

    area_widgets = T.Dict(
        help="a dictionary of child indices keyed by unique values of "
        "`area_attr` in SVG"
    ).tag(sync=True)

    visible_areas = T.Tuple(
        [None],
        help="a list of `area_attrs`s of SVG `g`s to show. " "Accepts [None] for all",
    ).tag(sync=True)

    zoom_x = T.Float().tag(sync=True)
    zoom_y = T.Float().tag(sync=True)
    zoom_k = T.Float().tag(sync=True)

    zoom_lock = T.Bool(
        False, help="Make children non-interactive for better pan/zoom"
    ).tag(sync=True)

    @T.observe("svg_file")
    def _on_svg_file_changed(self, *args, **kwargs):
        self.svg = Path(self.svg_file).read_text(encoding="utf-8")
