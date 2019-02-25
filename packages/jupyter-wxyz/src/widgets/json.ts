/* tslint:disable */
/// <reference path="../@types/jsonpointer/index.d.ts" />
/* tslint:enable */

import { FnModel } from './_base';
import * as jsonpointer from 'jsonpointer';
import Ajv from 'ajv';

const _ajv = new Ajv();

export class JSONModel extends FnModel<string, any, JSONModel.ITraits> {
  static model_name = 'JSONModel';

  defaults() {
    return {
      ...super.defaults(),
      _model_name: JSONModel.model_name,
      value: null as any
    };
  }

  async theFunction(source: string) {
    return JSON.parse(source);
  }
}

namespace JSONModel {
  export interface ITraits extends FnModel.ITraits<string, any> {}
}

export class JSONPointerModel extends FnModel<string, any, JSONModel.ITraits> {
  static model_name = 'JSONPointerModel';

  defaults() {
    return {
      ...super.defaults(),
      _model_name: JSONPointerModel.model_name,
      value: null as any,
      context: null as any
    };
  }

  async theFunction(source: string) {
    return jsonpointer.get(this.get('context'), source);
  }
}

namespace JSONPointerModel {
  export interface ITraits extends FnModel.ITraits<string, any> {
    context: Object;
  }
}

export class JSONSchemaModel extends FnModel<
  object,
  object,
  JSONSchema.ITraits
> {
  static model_name = 'JSONSchemaModel';

  defaults() {
    return {
      ...super.defaults(),
      _model_name: JSONSchemaModel.model_name,
      value: null as any,
      context: null as any
    };
  }

  async theFunction(source: object) {
    const validate = _ajv.compile(this.get('schema'));
    validate(source);
    if (validate.errors) {
      throw Error(validate.errors.join(''));
    }
    return source;
  }
}

namespace JSONSchema {
  export interface ITraits extends FnModel.ITraits<object, object> {
    schema: Object;
  }
}
