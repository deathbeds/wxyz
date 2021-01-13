import * as widgets from '@jupyter-widgets/base';

import { NAME, VERSION } from '..';
import { WXYZ } from '@deathbeds/wxyz-core';

export class FooModel extends widgets.DOMWidgetModel {
  static model_name = 'FooModel';
  static view_name = 'FooView';
  static model_module = NAME;
  static model_module_version = NAME;
  static view_module = VERSION;
  static view_module_version = VERSION;

  static serializers = {
    ...WXYZ.serializers,
  };

  defaults() {
    return {
      ...super.defaults(),
      _model_name: FooModel.model_name,
      _view_name: FooModel.view_name,
      _model_module: NAME,
      _model_module_version: VERSION,
      _view_module: NAME,
      _view_module_version: VERSION,
    };
  }
}

export class FooView extends widgets.DOMWidgetView {}
