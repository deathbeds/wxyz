import * as jsonld from 'jsonld';
import { Context, Frame, JsonLdArray } from 'jsonld/jsonld-spec';

import { JSONLDBase } from './_jsonld';

import { TObject } from '@deathbeds/wxyz-core';

export class ExpandModel extends JSONLDBase<
  TObject,
  JsonLdArray,
  ExpandModel.ITraits
> {
  static model_name = 'ExpandModel';

  defaults() {
    return { ...super.defaults(), _model_name: ExpandModel.model_name };
  }

  async theFunction(source: TObject) {
    const context = this.theExpandContext;
    const opts = context ? { expandContext: context } : {};
    return await jsonld.expand(source, opts);
  }
}

export class CompactModel extends JSONLDBase<
  TObject,
  TObject,
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

  async theFunction(source: TObject) {
    const expandContext = this.theExpandContext;
    const context = this.get('context') as Context;
    return (await jsonld.compact(source, context, {
      ...(expandContext ? { expandContext } : {}),
    })) as TObject;
  }
}

export class FlattenModel extends JSONLDBase<
  TObject,
  TObject,
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

  async theFunction(source: TObject) {
    const expandContext = this.theExpandContext;
    const context = this.get('context') as Context;
    return (await jsonld.flatten(source, context, {
      ...(expandContext ? { expandContext } : {}),
    })) as TObject;
  }
}

export class FrameModel extends JSONLDBase<
  TObject,
  TObject,
  FrameModel.ITraits
> {
  static model_name = 'FrameModel';

  defaults() {
    return { ...super.defaults(), _model_name: FrameModel.model_name };
  }

  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
    this.on('change:frame', this.theSourceChanged, this);
    return this;
  }

  async theFunction(source: TObject) {
    const frame = this.get('frame') as Frame;
    const framed = await jsonld.frame(source, frame);
    return framed as TObject;
  }
}

export class NormalizeModel extends JSONLDBase<
  TObject,
  TObject | string,
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

  async theFunction(source: TObject) {
    const expandContext = this.theExpandContext;
    const format = this.get('format');
    return await jsonld.normalize(source, {
      ...(expandContext ? { expandContext } : {}),
      ...(format ? { format } : {}),
    });
  }
}

export namespace ExpandModel {
  export interface ITraits<V = TObject, W = JsonLdArray>
    extends JSONLDBase.ITraits<V, W> {
    expand_context: TObject;
  }
}

export namespace CompactModel {
  export interface ITraits<V = TObject, W = TObject>
    extends JSONLDBase.ITraits<V, W> {
    context: Context;
  }
}

export namespace FlattenModel {
  export interface ITraits<V = TObject, W = TObject>
    extends JSONLDBase.ITraits<V, W> {
    context: Context;
  }
}

export namespace FrameModel {
  export interface ITraits<V = TObject, W = TObject>
    extends JSONLDBase.ITraits<V, W> {
    frame: Context;
  }
}

export namespace NormalizeModel {
  export interface ITraits<V = TObject, W = TObject | string>
    extends JSONLDBase.ITraits<V, W> {
    format: string;
  }
}
