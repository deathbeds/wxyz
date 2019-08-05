import { JSONModel } from '@deathbeds/wxyz-core/lib/widgets/json';
import { lazyLoader } from '@deathbeds/wxyz-core/lib/widgets/lazy';

const _jsone = lazyLoader(
  async () => await import(/* webpackChunkName: "json-e" */ 'json-e')
);

export class JSONEModel extends JSONModel {
  static model_name = 'JSONEModel';

  defaults() {
    return {
      ...super.defaults(),
      _model_name: JSONEModel.model_name,
      value: {} as any
    };
  }

  async theFunction(source: string) {
    const jsone = _jsone.get() || (await _jsone.load());
    const context = this.theContext;
    return jsone.default(JSON.parse(source), context);
  }

  get theContext() {
    return this.get('context');
  }

  set theContext(context: any) {
    this.set('context', context);
    this.save();
  }

  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
    this.on('change:context', this.theSourceChanged, this);
    this.theSourceChanged();
    return this;
  }
}
