import Ajv from 'ajv';
import jsonpointer from 'jsonpointer';

import { FnModel, TObject } from './_base';

const _ajv = new Ajv();

export class JSONModel extends FnModel<string, any, JSONModel.ITraits> {
  static model_name = 'JSONModel';

  defaults() {
    return {
      ...super.defaults(),
      _model_name: JSONModel.model_name,
      value: null as any,
    };
  }

  async theFunction(source: string) {
    return JSON.parse(source);
  }
}

export namespace JSONModel {
  export interface ITraits extends FnModel.ITraits<string, any> {}
}

export class UnJSONModel extends FnModel<any, string, UnJSONModel.ITraits> {
  static model_name = 'UnJSONModel';

  defaults() {
    return {
      ...super.defaults(),
      _model_name: UnJSONModel.model_name,
      source: null as any,
      value: '' as any,
      indent: null as any,
    };
  }

  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
    this.on('change:indent', this.theSourceChanged, this);
    return this;
  }

  async theFunction(source: any) {
    const indent: number = this.get('indent');
    return indent ? JSON.stringify(source, null, indent) : JSON.stringify(source);
  }
}

namespace UnJSONModel {
  export interface ITraits extends FnModel.ITraits<string, any> {}
}

export class JSONPointerModel extends FnModel<string, any, JSONModel.ITraits> {
  static model_name = 'JSONPointerModel';

  defaults() {
    return {
      ...super.defaults(),
      _model_name: JSONPointerModel.model_name,
      value: null as any,
      context: null as any,
    };
  }

  async theFunction(source: string) {
    return jsonpointer.get(this.get('context'), source);
  }
}

namespace JSONPointerModel {
  export interface ITraits extends FnModel.ITraits<string, any> {
    context: TObject;
  }
}

export class JSONSchemaModel extends FnModel<TObject, TObject, JSONSchema.ITraits> {
  static model_name = 'JSONSchemaModel';

  defaults() {
    return {
      ...super.defaults(),
      _model_name: JSONSchemaModel.model_name,
      value: null as any,
      context: null as any,
    };
  }

  async theFunction(source: TObject) {
    const validate = _ajv.compile(this.get('schema'));
    await validate(source);
    if (validate.errors) {
      throw Error(validate.errors.join(''));
    }
    return source;
  }
}

namespace JSONSchema {
  export interface ITraits extends FnModel.ITraits<TObject, TObject> {
    schema: TObject;
  }
}
