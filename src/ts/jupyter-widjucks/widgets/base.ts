import { DOMWidgetModel, ISerializers } from "@jupyter-widgets/base";

import * as V from "../version";

export class Model extends DOMWidgetModel {
  static model_module = V.MODULE_NAME;
  static model_module_version = V.MODULE_VERSION;
  static view_module = V.MODULE_NAME;
  static view_module_version = V.MODULE_VERSION;

  static serializers: ISerializers = { ...DOMWidgetModel.serializers };

  defaults() {
    return {
      ...super.defaults(),
      _model_module: V.MODULE_NAME,
      _model_module_version: V.MODULE_VERSION,
      _view_module: V.MODULE_NAME,
      _view_module_version: V.MODULE_VERSION
    };
  }
}

export class FnModel<T, U> extends Model {
  static model_name = "YAMLModel";

  defaults() {
    return { ...super.defaults(), value: null, source: "", error: "" };
  }

  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
    return this.on("change:source", this.source_changed, this);
  }

  theFunction(source: T): U {
    console.log(source);
    return (null as unknown) as U;
  }

  protected source_changed() {
    let changed = false;
    try {
      let value = this.theFunction(this.get("source"));
      if (value !== this.get("value")) {
        this.set("value", value);
        changed = true;
      }
      this.set("error", "");
    } catch (err) {
      this.set("err", `${err}`);
      changed = true;
    } finally {
      changed && this.save();
    }
    return this;
  }
}
