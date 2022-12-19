import { JSONModel, UnJSONModel } from '@deathbeds/wxyz-core';
import { lazyLoader } from '@deathbeds/wxyz-core';

const _yaml = lazyLoader(
  async () => await import(/* webpackChunkName: "js-yaml" */ 'js-yaml')
);

export class YAMLModel extends JSONModel {
  static model_name = 'YAMLModel';

  defaults(): any {
    return {
      ...super.defaults(),
      _model_name: YAMLModel.model_name,
      value: {} as any,
    };
  }

  async theFunction(source: string): Promise<any> {
    const { load, FAILSAFE_SCHEMA } = _yaml.get() || (await _yaml.load());
    return load(source, { schema: FAILSAFE_SCHEMA });
  }
}

export class UnYAMLModel extends UnJSONModel {
  static model_name = 'UnYAMLModel';

  defaults(): any {
    return {
      ...super.defaults(),
      _model_name: UnYAMLModel.model_name,
    };
  }

  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
    this.on('change:indent', this.theSourceChanged, this);
    return this;
  }

  async theFunction(source: string) {
    const { dump, FAILSAFE_SCHEMA } = _yaml.get() || (await _yaml.load());
    return dump(source, {
      indent: this.get('indent'),
      schema: FAILSAFE_SCHEMA,
    });
  }
}
