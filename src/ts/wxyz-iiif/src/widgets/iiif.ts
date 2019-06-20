import * as widgets from '@jupyter-widgets/base';

import { lazyLoader } from '@deathbeds/wxyz-core/lib/widgets/lazy';
import { WXYZ } from '@deathbeds/wxyz-core/lib/widgets/_base';

import { NAME, VERSION } from '..';

const _mirador = lazyLoader(
  async () => await import(/* webpackChunkName: "mirador" */ 'mirador')
);

export class IIIFModel extends WXYZ {
  static model_name = 'IIIFModel';
  static view_name = 'IIIFView';
  static model_module = NAME;
  static model_module_version = NAME;
  static view_module = VERSION;
  static view_module_version = VERSION;

  defaults() {
    return {
      ...super.defaults(),
      _model_name: IIIFModel.model_name,
      _view_name: IIIFModel.view_name,
      _model_module: NAME,
      _model_module_version: VERSION,
      _view_module: NAME,
      _view_module_version: VERSION
    };
  }
}

export class IIIFView extends widgets.DOMWidgetView {
  initialize(parameters: any) {
    super.initialize(parameters);
    console.log(_mirador);
    setTimeout(async () => {
      const mirador = _mirador.get() || (await _mirador.load());
      console.log(mirador);
    });
  }
}
