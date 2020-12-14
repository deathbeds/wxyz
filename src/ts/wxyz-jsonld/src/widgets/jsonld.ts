// this is a name-only import
import * as jsonld from 'jsonld';

import { JSONLDBase } from './_jsonld';

const { getJSONLD, loadJSONLD } = JSONLDBase;

export class ExpandModel extends JSONLDBase<
  object,
  object[],
  ExpandModel.ITraits
> {
  static model_name = 'ExpandModel';

  defaults() {
    return { ...super.defaults(), _model_name: ExpandModel.model_name };
  }

  async theFunction(source: object) {
    const context = this.theExpandContext;
    const opts = context ? { expandContext: context } : {};
    const { expand } = getJSONLD() || (await loadJSONLD());
    return await expand(source, opts);
  }
}

export class CompactModel extends JSONLDBase<
  object,
  object,
  CompactModel.ITraits
> {
  static model_name = 'CompactModel';

  defaults() {
    return { ...super.defaults(), _model_name: CompactModel.model_name };
  }

  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
    this.on('change:context', this.theSourceChanged, this);
    return this;
  }

  async theFunction(source: object) {
    const expandContext = this.theExpandContext;
    const context = this.get('context') as jsonld.IContext;
    const { compact } = getJSONLD() || (await loadJSONLD());
    return await compact(source, context, {
      ...(expandContext ? { expandContext } : {})
    });
  }
}

export class FlattenModel extends JSONLDBase<
  object,
  object,
  FlattenModel.ITraits
> {
  static model_name = 'FlattenModel';

  defaults() {
    return { ...super.defaults(), _model_name: FlattenModel.model_name };
  }

  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
    this.on('change:context', this.theSourceChanged, this);
    return this;
  }

  async theFunction(source: object) {
    const expandContext = this.theExpandContext;
    const context = this.get('context') as jsonld.IContext;
    const { flatten } = getJSONLD() || (await loadJSONLD());
    return await flatten(source, context, {
      ...(expandContext ? { expandContext } : {})
    });
  }
}

export class FrameModel extends JSONLDBase<object, object, FrameModel.ITraits> {
  static model_name = 'FrameModel';

  defaults() {
    return { ...super.defaults(), _model_name: FrameModel.model_name };
  }

  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
    this.on('change:frame', this.theSourceChanged, this);
    return this;
  }

  async theFunction(source: object) {
    const expandContext = this.theExpandContext;
    const frameContext = this.get('frame') as jsonld.IContext;
    const { frame } = getJSONLD() || (await loadJSONLD());
    return await frame(source, frameContext, {
      ...(expandContext ? { expandContext } : {})
    });
  }
}

export class NormalizeModel extends JSONLDBase<
  object,
  object | string,
  NormalizeModel.ITraits
> {
  static model_name = 'NormalizeModel';

  defaults() {
    return { ...super.defaults(), _model_name: NormalizeModel.model_name };
  }

  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
    this.on('change:format', this.theSourceChanged, this);
    return this;
  }

  async theFunction(source: object) {
    const expandContext = this.theExpandContext;
    const format = this.get('format');
    const { normalize } = getJSONLD() || (await loadJSONLD());
    return await normalize(source, {
      ...(expandContext ? { expandContext } : {}),
      ...(format ? { format } : {})
    });
  }
}

export namespace ExpandModel {
  export interface ITraits<V = object, W = object[]>
    extends JSONLDBase.ITraits<V, W> {
    expand_context: object;
  }
}

export namespace CompactModel {
  export interface ITraits<V = object, W = object>
    extends JSONLDBase.ITraits<V, W> {
    context: jsonld.IContext;
  }
}

export namespace FlattenModel {
  export interface ITraits<V = object, W = object>
    extends JSONLDBase.ITraits<V, W> {
    context: jsonld.IContext;
  }
}

export namespace FrameModel {
  export interface ITraits<V = object, W = object>
    extends JSONLDBase.ITraits<V, W> {
    frame: jsonld.IContext;
  }
}

export namespace NormalizeModel {
  export interface ITraits<V = object, W = object | string>
    extends JSONLDBase.ITraits<V, W> {
    format: string;
  }
}
