""" Widgets for working with Cytoscape
"""
# pylint: disable=too-many-ancestors,no-self-use,too-few-public-methods
from .base import CytoscapeBase, T, W


@W.register
class Cytoscape(CytoscapeBase, W.HBox):
    """ A Widget that renders Cytoscape JSON
    """

    _model_name = T.Unicode("CytoscapeModel").tag(sync=True)
    _view_name = T.Unicode("CytoscapeView").tag(sync=True)

    selected_elements = T.List().tag(sync=True)

    # // very commonly used options
    # elements: [ /* ... */ ],
    elements = T.List().tag(sync=True)
    # style: [ /* ... */ ],
    style_ = T.List().tag(sync=True)
    # layout: { name: 'grid' /* , ... */ },
    layout_name = T.Unicode("grid").tag(sync=True)
    layout_options = T.Dict().tag(sync=True)

    # // initial viewport state:
    # zoom: 1,
    zoom = T.Float(1.0).tag(sync=True)
    # pan: { x: 0, y: 0 },
    x = T.Float(0.0).tag(sync=True)
    y = T.Float(0.0).tag(sync=True)

    # // interaction options:
    # minZoom: 1e-50,
    min_zoom = T.Float(1e-50).tag(sync=True)
    # maxZoom: 1e50,
    max_zoom = T.Float(1e50).tag(sync=True)
    # zoomingEnabled: true,
    zooming_enabled = T.Bool(True).tag(sync=True)
    # userZoomingEnabled: true,
    user_zooming_enabled = T.Bool(True).tag(sync=True)
    # panningEnabled: true,
    panning_enabled = T.Bool(True).tag(sync=True)
    # userPanningEnabled: true,
    user_panning_enabled = T.Bool(True).tag(sync=True)
    # boxSelectionEnabled: false,
    box_selection_enabled = T.Bool(True).tag(sync=True)
    # selectionType: 'single',
    selection_type = T.Unicode("single").tag(sync=True)
    # touchTapThreshold: 8,
    touch_tap_threshold = T.Int(8).tag(sync=True)
    # desktopTapThreshold: 4,
    desktop_tap_threshold = T.Int(4).tag(sync=True)
    # autolock: false,
    autolock = T.Bool(False).tag(sync=True)
    # autoungrabify: false,
    autoungrabify = T.Bool(False).tag(sync=True)
    # autounselectify: false,
    autounselectify = T.Bool(False).tag(sync=True)

    # // rendering options:
    # headless: false,
    headless = T.Bool(False).tag(sync=True)
    # styleEnabled: true,
    style_enabled = T.Bool(False).tag(sync=True)
    # hideEdgesOnViewport: false,
    hide_edges_on_viewport = T.Bool(False).tag(sync=True)
    # hideLabelsOnViewport: false,
    hide_labels_on_viewport = T.Bool(False).tag(sync=True)
    # textureOnViewport: false,
    texture_on_viewport = T.Bool(False).tag(sync=True)
    # motionBlur: false,
    motion_blur = T.Bool(False).tag(sync=True)
    # motionBlurOpacity: 0.2,
    motion_blur_opacity = T.Float(0.2).tag(sync=True)
    # wheelSensitivity: 1,
    wheel_sensitivity = T.Int(1).tag(sync=True)
    # pixelRatio: 'auto'
    pixel_ratio = T.Unicode("auto").tag(sync=True)
