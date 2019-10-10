import { DOMWidgetView, DOMWidgetModel } from '@jupyter-widgets/base';

import { Core } from 'cytoscape';
import { lazyLoader } from '@deathbeds/wxyz-core/lib/widgets/lazy';
import { Throttler } from '@jupyterlab/coreutils';

import { NAME, VERSION } from '..';

const CYTOSCAPE_CLASS = 'jp-WXYZ-Cytoscape';

const _cytoscape = lazyLoader(async () => {
  return (await import(/* webpackChunkName: "cytoscape" */ 'cytoscape'))
    .default;
});

const _elk = lazyLoader(async () => {
  return (await import(/* webpackChunkName: "cytoscape" */ 'cytoscape-elk'))
    .default;
});

interface ICyCallable {
  (m: CytoscapeModel, cy: Core): void;
}

interface ICyCallMap {
  [key: string]: ICyCallable;
}

function renamed(wname: string, cname: string): ICyCallMap {
  return {
    [wname]: (m, cy) => cy.json({ [cname]: m.get(wname) })
  };
}

let CY_MAP: ICyCallMap = {
  style_: (m, cy) => cy.style(m.get('style_') || {}),
  layout_name: (m, cy) => {
    const name = m.get('layout_name');
    const opts = m.get('layout_options') || {};
    cy.layout({ ...opts, name: name ? name : opts.name }).run();
  },
  x: (m, cy) => cy.pan({ x: m.get('x') || 0, y: m.get('y') || 0 }),
  ...renamed('min_zoom', 'minZoom'),
  ...renamed('max_zoom', 'maxZoom'),
  ...renamed('zooming_enabled', 'zoomingEnabled'),
  ...renamed('user_zooming_enabled', 'userZoomingEnabled'),
  ...renamed('panning_enabled', 'panningEnabled'),
  ...renamed('box_selection_enabled', 'boxSelectionEnabled'),
  ...renamed('touch_tap_threshold', 'touchTapThreshold'),
  ...renamed('desktop_tap_threshold', 'desktopTapThreshold'),
  ...renamed('style_enabled', 'styleEnabled'),
  ...renamed('hide_edges_on_viewport', 'hideEdgesOnViewport'),
  ...renamed('hide_labels_on_viewport', 'hideLabelsOnViewport'),
  ...renamed('texture_on_viewport', 'textureOnViewport'),
  ...renamed('motion_blur', 'motionBlur'),
  ...renamed('motion_blur_opacity', 'motionBlurOpacity'),
  ...renamed('wheel_sensitivity', 'wheelSensitivity'),
  ...renamed('pixel_ratio', 'pixelRatio')
};

CY_MAP.y = CY_MAP.x;
CY_MAP.layout_options = CY_MAP.layout_name;

export class CytoscapeModel extends DOMWidgetModel {
  static model_name = 'CytoscapeModel';
  static view_name = 'CytoscapeView';
  static model_module = NAME;
  static model_module_version = NAME;
  static view_module = VERSION;
  static view_module_version = VERSION;

  cyDefaults() {
    return {
      // # // very commonly used options
      // # elements: [ /* ... */ ],
      // elements = T.List().tag(sync=True)
      elements: [] as any[],
      // # style: [ /* ... */ ],
      // style_ = T.List().tag(sync=True)
      style_: [] as any[],
      // # layout: { name: 'grid' /* , ... */ },
      // layout_name = T.Unicode("grid").tag(sync=True)
      layout_name: 'grid',
      // layout_options = T.Dict().tag(sync=True)
      layout_options: {},
      // # // initial viewport state:
      // # zoom: 1,
      // zoom = T.Float(1.0).tag(sync=True)
      zoom: 1,
      // # pan: { x: 0, y: 0 },
      // x = T.Float(0.0).tag(sync=True)
      // y = T.Float(0.0).tag(sync=True)
      x: 0.0,
      y: 0.0,
      // # // interaction options:
      // # minZoom: 1e-50,
      // min_zoom = T.Float(1e-50).tag(sync=True)
      min_zoom: 1e-50,
      // # maxZoom: 1e50,
      // max_zoom = T.Float(1e50).tag(sync=True)
      max_zoom: 1e50,
      // # zoomingEnabled: true,
      // zooming_enabled = T.Bool(True).tag(sync=True)
      zooming_enabled: true,
      // # userZoomingEnabled: true,
      // user_zooming_enabled = T.Bool(True).tag(sync=True)
      user_zooming_enabled: true,
      // # panningEnabled: true,
      // panning_enabled = T.Bool(True).tag(sync=True)
      panning_enabled: true,
      // # userPanningEnabled: true,
      // user_panning_enabled = T.Bool(True).tag(sync=True)
      user_panning_enabled: true,
      // # boxSelectionEnabled: false,
      // box_selection_enabled = T.Bool(True).tag(sync=True)
      box_selection_enabled: true,
      // # selectionType: 'single',
      // selection_type = T.Unicode("single").tag(sync=True)
      selection_type: 'single',
      // # touchTapThreshold: 8,
      // touch_tap_threshold = T.Int(8).tag(sync=True)
      touch_tap_threshold: 8,
      // # desktopTapThreshold: 4,
      // desktop_tap_threshold = T.Int(4).tag(sync=True)
      desktop_tap_threshold: 4,
      // # autolock: false,
      // autolock = T.Bool(False).tag(sync=True)
      autolock: false,
      // # autoungrabify: false,
      // autoungrabify = T.Bool(False).tag(sync=True)
      autoungrabify: false,
      // # autounselectify: false,
      // autounselectify = T.Bool(False).tag(sync=True)
      autounselectify: false,

      // # // rendering options:
      // # headless: false,
      // headless = T.Bool(False).tag(sync=True)
      headless: false,
      // # styleEnabled: true,
      // style_enabled = T.Bool(False).tag(sync=True)
      style_enabled: true,
      // # hideEdgesOnViewport: false,
      // hide_edges_on_viewport = T.Bool(False).tag(sync=True)
      hide_edges_on_viewport: false,
      // # hideLabelsOnViewport: false,
      // hide_labels_on_viewport = T.Bool(False).tag(sync=True)
      hide_labels_on_viewport: false,
      // # textureOnViewport: false,
      // texture_on_viewport = T.Bool(False).tag(sync=True)
      texture_on_viewport: false,
      // # motionBlur: false,
      // motion_blur = T.Bool(False).tag(sync=True)
      motion_blur: false,
      // # motionBlurOpacity: 0.2,
      // motion_blur_opacity = T.Float(0.2).tag(sync=True)
      motion_blur_opacity: 0.2,
      // # wheelSensitivity: 1,
      // wheel_sensitivity = T.Int(1).tag(sync=True)
      wheel_sensitivity: 1,
      // # pixelRatio: 'auto'
      // pixel_ratio = T.Unicode("auto").tag(sync=True)
      pixel_ratio: 'auto'
    };
  }

  defaults() {
    return {
      ...super.defaults(),
      _model_name: CytoscapeModel.model_name,
      _model_module: NAME,
      _model_module_version: VERSION,
      _view_module: NAME,
      _view_module_version: VERSION,
      ...this.cyDefaults()
    };
  }
}

export class CytoscapeView extends DOMWidgetView {
  private _cytoscape: Core;
  private _throttledSelect: Throttler;

  render() {
    super.render();
    this.pWidget.addClass(CYTOSCAPE_CLASS);

    this.displayed
      .then(async () => await this.initCytoscape())
      .catch(err => console.error('CytoscapeView error', err));
  }

  remove() {
    super.remove();
    this._throttledSelect.dispose();
  }

  async initCytoscape() {
    await Promise.all([_cytoscape.load(), _elk.load()]);
    const _cyto = _cytoscape.get();
    const elk = _elk.get();
    this._cytoscape = _cyto({ container: this.el });
    _cyto.use(elk);

    // http://js.cytoscape.org/#events/collection-events
    this._throttledSelect = new Throttler(() => this.onSelect(), 100);
    this._cytoscape.on('select', () => this._throttledSelect.invoke());

    const handlers = Object.keys(
      (this.model as CytoscapeModel).cyDefaults()
    ).map(f => {
      let handler = () => {
        const handler = CY_MAP[f] || ((m, obj) => obj.json({ [f]: m.get(f) }));
        handler(this.model as CytoscapeModel, this._cytoscape);
      };
      this.model.on(`change:${f}`, handler);
      return handler;
    });

    handlers.map(h => h());
  }

  onSelect() {
    const selected = this._cytoscape.$(':selected');
    this.model.set('selected_elements', selected.jsons());
    this.touch();
  }
}
