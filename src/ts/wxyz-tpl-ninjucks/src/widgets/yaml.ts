import { JSONModel } from './json';
import { lazyLoader } from './lazy';

const _yaml = lazyLoader(
  async () => await import(/* webpackChunkName: "js-yaml" */ 'js-yaml')
);

export class YAMLModel extends JSONModel {
  static model_name = 'YAMLModel';

  defaults() {
    return {
      ...super.defaults(),
      _model_name: YAMLModel.model_name,
      value: {} as any
    };
  }

  async theFunction(source: string) {
    const { safeLoad } = _yaml.get() || (await _yaml.load());
    return safeLoad(source);
  }
}
