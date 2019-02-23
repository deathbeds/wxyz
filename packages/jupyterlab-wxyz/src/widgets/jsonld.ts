import * as jsonld from 'jsonld';

import { JSONLDBase } from './_jsonld';

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
    return await jsonld.expand(source, opts);
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
    this.on('change:context_changed', this.theSourceChanged, this);
    this.theSourceChanged();
    return this;
  }

  async theFunction(source: object) {
    const expandContext = this.theExpandContext;
    const context = this.get('context') as jsonld.IContext;
    return await jsonld.compact(source, context, {
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
    this.on('change:context_changed', this.theSourceChanged, this);
    this.theSourceChanged();
    return this;
  }

  async theFunction(source: object) {
    const expandContext = this.theExpandContext;
    const context = this.get('context') as jsonld.IContext;
    return await jsonld.flatten(source, context, {
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
    this.on('change:frame_changed', this.theSourceChanged, this);
    this.theSourceChanged();
    return this;
  }

  async theFunction(source: object) {
    const expandContext = this.theExpandContext;
    const frame = this.get('frame') as jsonld.IContext;
    return await jsonld.frame(source, frame, {
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
    this.on('change:format_changed', this.theSourceChanged, this);
    this.theSourceChanged();
    return this;
  }

  async theFunction(source: object) {
    const expandContext = this.theExpandContext;
    const format = this.get('format');
    return await jsonld.normalize(source, {
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
