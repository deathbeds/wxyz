import * as nunjucks from "nunjucks";

import {
  WidgetModel,
  unpack_models as deserialize
} from "@jupyter-widgets/base";

import { FnModel } from "./base";

nunjucks.installJinjaCompat();

export class TemplateModel extends FnModel<string, string> {
  static model_name = "TemplateModel";
  static serializers = { ...FnModel.serializers, context: { deserialize } };

  defaults() {
    return {
      ...super.defaults(),
      _model_name: TemplateModel.model_name,
      value: "",
      context: null
    };
  }

  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
    this.on("change:context", this.context_changed, this).context_changed();

    return this.source_changed();
  }

  protected context_changed() {
    let previous = (this.previousAttributes() as any) || {};
    if (previous.context) {
      (previous.context as WidgetModel).off(void 0, void 0, this);
    }
    let context = this.get("context") as WidgetModel;
    if (context && context.on) {
      context.on("change", this.source_changed, this);
    }
    return this.source_changed();
  }

  theFunction(source: string) {
    let contextWidget: WidgetModel = this.get("context");
    let context = contextWidget ? contextWidget.attributes : {};
    return nunjucks.renderString(source || "", context);
  }
}
