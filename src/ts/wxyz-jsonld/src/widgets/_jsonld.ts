import * as jsonld from 'jsonld';

import { FnModel } from '@deathbeds/wxyz-core/lib/widgets/_base';
import { lazyLoader } from '@deathbeds/wxyz-core/lib/widgets/lazy';

export class JSONLDBase<T, U, V extends FnModel.ITraits<T, U>> extends FnModel<
  T,
  U,
  V
> {
  static model_name = 'ExpandModel';

  defaults() {
    return {
      ...super.defaults(),
      expand_context: null as jsonld.IContext,
    };
  }

  get theExpandContext() {
    return this.get('expand_context');
  }
  set theExpandContext(context: jsonld.IContext) {
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
  export interface ITraits<T = object, U = object>
    extends FnModel.ITraits<T, U> {
    expandContext: jsonld.IContext;
  }

  const _jsonld = lazyLoader(
    async () => await import(/* webpackChunkName: "jsonld" */ 'jsonld')
  );

  export function getJSONLD() {
    return _jsonld.get();
  }
  export function loadJSONLD() {
    return _jsonld.load();
  }
}
