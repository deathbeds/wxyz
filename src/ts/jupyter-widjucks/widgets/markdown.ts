import marked from "marked";

import { FnModel } from "./base";

export class MarkdownModel extends FnModel<string, string> {
  static model_name = "MarkdownModel";

  defaults() {
    return {
      ...super.defaults(),
      _model_name: MarkdownModel.model_name,
      value: {}
    };
  }

  theFunction(source: string) {
    return marked.parse(source);
  }
}
