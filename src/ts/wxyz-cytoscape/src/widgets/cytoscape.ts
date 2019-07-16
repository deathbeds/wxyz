import { DOMWidgetView, DOMWidgetModel } from '@jupyter-widgets/base';

import { Core } from 'cytoscape';
import { lazyLoader } from '@deathbeds/wxyz-core/lib/widgets/lazy';

import { NAME, VERSION } from '..';

const CYTOSCAPE_CLASS = 'jp-WXYZ-Cytoscape';

const _cytoscape = lazyLoader(async () => {
  return (await import(/* webpackChunkName: "cytoscape" */ 'cytoscape'))
    .default;
});

export class CytoscapeModel extends DOMWidgetModel {
  static model_name = 'CytoscapeModel';
  static view_name = 'CytoscapeView';
  static model_module = NAME;
  static model_module_version = NAME;
  static view_module = VERSION;
  static view_module_version = VERSION;

  defaults() {
    return {
      ...super.defaults(),
      _model_name: CytoscapeModel.model_name,
      value: {
        elements: {
          nodes: [],
          edges: []
        },
        data: {
          data: 'Untitled Graph'
        }
      } as any
    };
  }
}

export class CytoscapeView extends DOMWidgetView {
  private _cytoscape: Core;

  async render() {
    super.render();
    this.pWidget.addClass(CYTOSCAPE_CLASS);

    this.model.on('change:value', this.value_changed, this);

    this._cytoscape = (_cytoscape.get() || (await _cytoscape.load()))({
      container: this.el,
      elements: this.model.get('value'),
      style: this.model.get('style'),
      layout: this.model.get('layout')
    });

    this.value_changed();
  }

  async value_changed() {
    console.log('value changed', arguments, this._cytoscape);
  }
}
