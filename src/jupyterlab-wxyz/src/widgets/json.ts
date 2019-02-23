import { FnModel } from "./base";

export class JSONModel extends FnModel<string, any, JSONModel.ITraits> {
  static model_name = "JSONModel";

  defaults() {
    return {
      ...super.defaults(),
      _model_name: JSONModel.model_name,
      value: null as any
    };
  }

  theFunction(source: string) {
    return JSON.parse(source);
  }
}

namespace JSONModel {
  export interface ITraits extends FnModel.ITraits<string, any> {}
}
