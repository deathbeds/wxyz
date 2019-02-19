import { FnModel } from "./base";
import { safeLoad } from "js-yaml";

export class YAMLModel extends FnModel<string, any> {
  static model_name = "YAMLModel";

  defaults() {
    return {
      ...super.defaults(),
      _model_name: YAMLModel.model_name,
      value: {}
    };
  }

  theFunction(source: string) {
    return safeLoad(source);
  }
}
