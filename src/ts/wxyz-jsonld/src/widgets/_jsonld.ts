import { Context } from 'jsonld/jsonld-spec';

import { FnModel, TObject } from '@deathbeds/wxyz-core/lib/widgets/_base';

export class JSONLDBase<T, U, V extends FnModel.ITraits<T, U>> extends FnModel<
  T,
  U,
  V
> {
  static model_name = 'ExpandModel';

  defaults() {
    return {
      ...super.defaults(),
      expand_context: null as Context,
    };
  }

  get theExpandContext() {
    return this.get('expand_context');
  }
  set theExpandContext(context: Context) {
    this.set('expand_context', context);
    this.save();
  }

  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
    this.on('change:expand_context', this.theSourceChanged, this);
    return this;
  }
}

export namespace JSONLDBase {
  export interface ITraits<T = TObject, U = TObject>
    extends FnModel.ITraits<T, U> {
    expandContext: Context;
  }
}
