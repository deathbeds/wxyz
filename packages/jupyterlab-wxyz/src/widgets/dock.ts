import { unpack_models as deserialize } from '@jupyter-widgets/base';

import { BoxModel, BoxView } from '@jupyter-widgets/controls';
import { DockLayout } from '@phosphor/widgets';

import { NAME, VERSION } from '..';

import { JupyterPhosphorDockPanelWidget } from './_dock';

export class DockBoxModel extends BoxModel {
  static model_name = 'DockBoxModel';
  static model_module = NAME;
  static model_module_version = VERSION;
  static view_name: 'DockBoxView';
  static view_module = NAME;
  static view_module_version = VERSION;

  static serializers = {
    ...BoxModel.serializers,
    dock_layout: { deserialize }
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
      dock_layout: null as DockLayout.AreaConfig
    };
  }
}

export class DockBoxView extends BoxView {
  _createElement(tagName: string) {
    this.pWidget = new JupyterPhosphorDockPanelWidget({ view: this }) as any;
    return this.pWidget.node;
  }
}
