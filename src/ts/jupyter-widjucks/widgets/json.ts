import { FnModel } from "./base";

export class JSONModel extends FnModel<string, any> {
  static model_name = "JSONModel";

  defaults() {
    return {
      ...super.defaults(),
      _model_name: JSONModel.model_name,
      value: {}
    };
  }

  theFunction(source: string) {
    return JSON.parse(source);
  }
}
