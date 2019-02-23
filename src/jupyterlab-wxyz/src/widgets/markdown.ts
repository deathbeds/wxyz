import marked from "marked";

import { FnModel } from "./base";

export class MarkdownModel extends FnModel<
  string,
  string,
  MarkdownModel.ITraits
> {
  static model_name = "MarkdownModel";

  defaults() {
    return {
      ...super.defaults(),
      _model_name: MarkdownModel.model_name
    };
  }

  theFunction(source: string) {
    return marked.parse(source);
  }
}

export namespace MarkdownModel {
  export interface ITraits extends FnModel.ITraits<string, string> {}
}
