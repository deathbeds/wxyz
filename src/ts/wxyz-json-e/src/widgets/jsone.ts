import { FnModel, TObject } from '@deathbeds/wxyz-core/lib/widgets/_base';
import { JSONExt } from '@lumino/coreutils';
import jsone from 'json-e';

export class JSONEModel extends FnModel<TObject, any, JSONEModel.ITraits> {
  static model_name = 'JSONEModel';

  defaults() {
    return {
      ...super.defaults(),
      _model_name: JSONEModel.model_name,
      value: {} as any,
      context: {} as any,
    };
  }

  async theFunction(source: TObject) {
    const context = this.theContext;
    const result = jsone(source, context);
    return result;
  }

  get theContext() {
    return this.get('context');
  }

  set theContext(context: any) {
    if (context == null || JSONExt.deepEqual(context, this.get('context'))) {
      return;
    }
    this.set('context', context);
    this.save();
  }

  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
    this.on('change:context', this.theSourceChanged, this);
    return this;
  }
}

export namespace JSONEModel {
  export interface ITraits extends FnModel.ITraits<TObject, TObject> {}
}
