""" Widgets that render in the dock
"""
# pylint: disable=too-many-ancestors
from ._base import Base, T, W


@W.register
class DockBox(Base, W.Box):
    """ A Box that renders as a DockPanel
    """

    _model_name = T.Unicode("DockBoxModel").tag(sync=True)
    _view_name = T.Unicode("DockBoxView").tag(sync=True)

    dock_layout = T.Dict(
        help=""" An AreaConfig from `DockPanel.saveLayout` from `@phosphor/widgets`,
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
    ).tag(
        sync=True,
        **W.widget_serialization,
    )
