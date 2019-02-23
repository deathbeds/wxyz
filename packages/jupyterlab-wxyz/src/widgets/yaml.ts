import { safeLoad } from 'js-yaml';

import { JSONModel } from './json';

export class YAMLModel extends JSONModel {
  static model_name = 'YAMLModel';

  defaults() {
    return {
      ...super.defaults(),
      _model_name: YAMLModel.model_name,
      value: {} as any
    };
  }

  theFunction(source: string) {
    return safeLoad(source);
  }
}
