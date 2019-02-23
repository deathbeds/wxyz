import * as jsonld from 'jsonld';

import { FnModel } from './base';

export class ExpandModel extends FnModel<object, object, ExpandModel.ITraits> {
  static model_name = 'ExpandModel';

  defaults() {
    return {
      ...super.defaults(),
      _model_name: ExpandModel.model_name,
      context: null as object
    };
  }

  async theFunction(source: object) {
    const context = this.get('context');
    const opts = context ? { expandContext: context } : {};
    this.theValue = jsonld.expand(source, opts);
  }

  get theContext() {
    return this.get('context');
  }
  set theContext(context: object) {
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

export namespace ExpandModel {
  export interface ITraits extends FnModel.ITraits<object, object> {
    context: object;
  }
}
