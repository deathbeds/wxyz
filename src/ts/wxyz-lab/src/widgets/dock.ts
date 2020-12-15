import screenfull from 'screenfull';

import { unpack_models as deserialize } from '@jupyter-widgets/base';

import { BoxModel, BoxView } from '@jupyter-widgets/controls';
import { DockLayout } from '@lumino/widgets';

import { NAME, VERSION } from '..';

import {
  JupyterPhosphorDockPanelWidget,
  JupyterLabPhosphorDockPanelWidget,
} from './_dock';

export class DockBoxModel extends BoxModel {
  static model_name = 'DockBoxModel';
  static model_module = NAME;
  static model_module_version = VERSION;
  static view_name: 'DockBoxView';
  static view_module = NAME;
  static view_module_version = VERSION;

  static serializers = {
    ...BoxModel.serializers,
    dock_layout: { deserialize },
  };

  defaults() {
    return {
      ...super.defaults(),
      _model_module: NAME,
      _model_module_version: VERSION,
      _view_module: NAME,
      _view_module_version: VERSION,
      _model_name: DockBoxModel.model_name,
      _view_name: DockBoxModel.view_name,
      dock_layout: null as DockLayout.AreaConfig,
      tab_size: null,
      border: null,
      hide_tabs: null,
    };
  }
}

export class DockBoxView extends BoxView {
  private _childrenInitialized = false;

  render() {
    super.render();

    if (this._childrenInitialized) {
      return;
    }

    const originalLayout = this.model.get('dock_layout');

    // handle initial child readiness for `dock_layout`
    Promise.all(this.children_views.views)
      .then(async () => {
        if (originalLayout != null) {
          await (this.pWidget as any).onLayoutModelChanged(originalLayout);
        }
        this._childrenInitialized = true;
      })
      .catch((err) => {
        console.error(err);
      });
  }

  _createElement(tagName: string) {
    this.pWidget = new JupyterPhosphorDockPanelWidget({ view: this }) as any;
    this.pWidget.node.addEventListener('click', (evt: MouseEvent) => {
      if (evt.shiftKey) {
        const anyful = screenfull as any;
        if (anyful && anyful.enabled) {
          anyful.toggle(this.pWidget.node);
        }
      }
    });
    return this.pWidget.node;
  }
}

export class DockPopModel extends BoxModel {
  static model_name = 'DockPopModel';
  static model_module = NAME;
  static model_module_version = VERSION;
  static view_name: 'DockPopView';
  static view_module = NAME;
  static view_module_version = VERSION;
}

export class DockPopView extends BoxView {
  _createElement(tagName: string) {
    let pWidget = new JupyterLabPhosphorDockPanelWidget({ view: this }) as any;
    this.pWidget = pWidget;
    pWidget.app = (DockPopView as any)['app'];
    return pWidget.node;
  }
}
