import { BoxModel, BoxView } from "@jupyter-widgets/controls";

import * as V from "../version";

import { JupyterPhosphorDockPanelWidget } from "./_dock";

export class DockBoxModel extends BoxModel {
  static model_name = "DockBoxModel";
  static model_module = V.MODULE_NAME;
  static model_module_version = V.MODULE_VERSION;
  static view_name: "DockBoxView";
  static view_module = V.MODULE_NAME;
  static view_module_version = V.MODULE_VERSION;

  defaults() {
    return {
      ...super.defaults(),
      _model_module: V.MODULE_NAME,
      _model_module_version: V.MODULE_VERSION,
      _view_module: V.MODULE_NAME,
      _view_module_version: V.MODULE_VERSION,
      _model_name: DockBoxModel.model_name,
      _view_name: DockBoxModel.view_name
    };
  }
}

export class DockBoxView extends BoxView {
  _createElement(tagName: string) {
    this.pWidget = new JupyterPhosphorDockPanelWidget({ view: this }) as any;
    return this.pWidget.node;
  }
}
