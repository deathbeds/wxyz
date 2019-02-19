import {WidgetModel, ISerializers} from '@jupyter-widgets/base';

import * as V from '../version';


export class Model extends WidgetModel {
  static model_module = V.MODULE_NAME;
  static model_module_version = V.MODULE_VERSION;

  static serializers: ISerializers = {...WidgetModel.serializers}


  defaults() {
    return {...super.defaults(),
      _model_module: V.MODULE_NAME,
      _model_module_version: V.MODULE_VERSION
    };
  }
}
