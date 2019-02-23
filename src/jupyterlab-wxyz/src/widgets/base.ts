import { DOMWidgetModel, ISerializers } from "@jupyter-widgets/base";

import {NAME, VERSION} from "..";

export class Model<T> extends DOMWidgetModel {
  static model_module = NAME;
  static model_module_version = VERSION;
  static view_module = NAME;
  static view_module_version = VERSION;

  static serializers: ISerializers = { ...DOMWidgetModel.serializers };

  defaults(): T {
    return {
      ...super.defaults(),
      _model_module: NAME,
      _model_module_version: VERSION,
      _view_module: NAME,
      _view_module_version: VERSION,
      icon_class: "jp-CircleIcon",
      description: "An Undescribed Widget",
      closable: true
    };
  }
}

export namespace Model {
  export interface ITraits {
    _model_module: string;
    _model_module_version: string;
    _view_module: string;
    _view_module_version: string;
    _view_name: string | null;
    _view_count: number;
    icon_class: string;
    description: string;
    closable: boolean;
  }
}

export class FnModel<T, U, V extends FnModel.ITraits<T, U>> extends Model<V> {
  static model_name = "FnModel";

  defaults() {
    return {
      ...super.defaults(),
      source: (null as unknown) as T,
      value: (null as unknown) as U,
      error: (null as unknown) as string
    };
  }

  initialize(attributes: V, options: any) {
    super.initialize(attributes, options);
    return this.on("change:source", this.theSourceChanged, this);
  }

  theFunction(source: T): U {
    console.error("undeFned", source);
    return (null as unknown) as U;
  }

  get theSource(): T {
    return this.get("source");
  }
  set theSource(src: T) {
    this.set("source", src);
    this.save();
  }

  get theValue(): U {
    return this.get("value");
  }
  set theValue(val: U) {
    this.set("value", val);
    this.save();
  }

  get theError(): string {
    return this.get("error");
  }

  set theError(err: string) {
    this.set("error", err);
    this.save();
  }

  protected theSourceChanged() {
    let changed = false;
    let err = "";
    try {
      let value = this.theFunction(this.theSource);
      if (value !== this.theValue) {
        this.theValue = value;
        changed = true;
      }
    } catch (err) {
      changed = true;
    }
    this.theError = err;
    changed && this.save();
    return this;
  }
}

export namespace FnModel {
  export interface ITraits<T, U> extends Model.ITraits {
    value: T;
    source: U;
    error: string;
  }
}
