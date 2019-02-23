import CodeMirror from "codemirror";

import { DOMWidgetView } from "@jupyter-widgets/base";
import { TextareaModel } from "@jupyter-widgets/controls";

import * as V from "../version";

export class EditorModel extends TextareaModel {
  static model_name = "EditorModel";
  static model_module = V.MODULE_NAME;
  static model_module_version = V.MODULE_VERSION;
  static view_name = "EditorView";
  static view_module = V.MODULE_NAME;
  static view_module_version = V.MODULE_VERSION;

  defaults() {
    return {
      ...super.defaults(),
      _model_name: EditorModel.model_name,
      _model_module: V.MODULE_NAME,
      _model_module_version: V.MODULE_VERSION,
      _view_name: EditorModel.view_name,
      _view_module: V.MODULE_NAME,
      _view_module_version: V.MODULE_VERSION,
      description: "An Editor",
      icon_class: "jp-EditIcon"
    };
  }
}

export class EditorView extends DOMWidgetView {
  private _editor: CodeMirror.Editor = null as any;
  private _editorNode: HTMLElement = null as any;

  render() {
    super.render();
    this.el.style.display = "flex";
    this.el.style.flexDirection = "column";
    this._editorNode = document.createElement("div");
    this._editorNode.style.flex = "1";
    this.el.appendChild(this._editorNode);
    this._editor = CodeMirror(this._editorNode);
    this._editor.on("change", () => {
      this.model.set("value", this._editor.getValue());
      this.touch();
    });
    this.model.on("change:value", this.value_changed, this);
    setTimeout(() => {
      this._editor.refresh();
      this.value_changed();
    }, 1);
  }

  value_changed() {
    if (this._editor.getValue() !== this.model.get("value")) {
      this._editor.setValue(this.model.get("value"));
    }
  }
}
