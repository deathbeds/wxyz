""" Widgets that render in the dock
"""
from .base import LabBase, T, W

DOCK_LAYOUT_HELP = """
An `AreaConfig` from `DockPanel.saveLayout` from `@lumino/widgets`,
e.g.
{
    "type": "split-area",
    "orientation": "orientation",
    "sizes": [1, 1, 1, 1]
    "children": [
        {"type": "tab-area", "widgets": [0], "currentIndex": 0},
        {"type": "tab-area", "widgets": [1], "currentIndex": 0},
        {"type": "tab-area", "widgets": [2], "currentIndex": 0},
        {"type": "tab-area", "widgets": [3], "currentIndex": 0}
    ]
}

The `widgets` list of a `tab-area` should be indices of `children`
"""


@W.register
class DockBox(LabBase, W.Box):
    """A `Box` that renders as a `DockPanel`"""

    _model_name = T.Unicode("DockBoxModel").tag(sync=True)
    _view_name = T.Unicode("DockBoxView").tag(sync=True)

    dock_layout = T.Dict(help=DOCK_LAYOUT_HELP).tag(sync=True)
    hide_tabs = T.Bool(False).tag(sync=True)
    tab_size = T.Unicode(help="CSS size value for tab bars", allow_none=True).tag(
        sync=True
    )
    border_size = T.Unicode(
        help="CSS size value for border width", allow_none=True
    ).tag(sync=True)
    spacing = T.Float(help="Spacing between children", allow_none=True).tag(sync=True)


MODES = """
tab-after
tab-before
split-top
split-left
split-right
split-bottom
""".strip().split(
    "\n"
)


@W.register
class DockPop(LabBase, W.Box):
    """A "box" that just adds stuff to the main JupyterLab area"""

    mode = T.Enum(MODES, default_value=None, allow_none=True).tag(sync=True)

    _model_name = T.Unicode("DockPopModel").tag(sync=True)
    _view_name = T.Unicode("DockPopView").tag(sync=True)
