import * as React from 'react';
import * as ReactDOM from 'react-dom';

import { DOMWidgetView, DOMWidgetModel } from '@jupyter-widgets/base';

import { IconName } from '@blueprintjs/icons';
import { Icon } from '@blueprintjs/core';

import { NAME, VERSION } from '../..';

const h = React.createElement;

const ICON_CLASS = 'jp-WXYZ-Blueprint-Icon';

export class IconModel extends DOMWidgetModel {
  static model_name = 'IconModel';
  static model_module = NAME;
  static model_module_version = VERSION;
  static view_name = 'IconView';
  static view_module = NAME;
  static view_module_version = VERSION;

  get icon(): IconName {
    return this.get('icon');
  }

  get color(): string {
    return this.get('color') || 'var(--jp-ui-font-color1)';
  }

  get iconSize(): number {
    return this.get('icon_size');
  }

  defaults() {
    return {
      ...super.defaults(),
      _model_name: IconModel.model_name,
      _model_module: NAME,
      _model_module_version: VERSION,
      _view_name: IconModel.view_name,
      _view_module: NAME,
      _view_module_version: VERSION,
      description: 'An Icon',
      icon: 'blank',
      color: 'var(--jp-ui-font-color1)',
      icon_size: 20
    };
  }

  static asComponent(m: IconModel) {
    const { icon, color, iconSize } = m;
    return h(Icon, { icon, color, iconSize });
  }
}

export class IconView extends DOMWidgetView {
  render() {
    super.render();
    this.pWidget.addClass(ICON_CLASS);
    this.model.on('change', this.rerender, this);
    this.rerender();
  }

  get m() {
    return this.model as IconModel;
  }

  rerender() {
    ReactDOM.render(IconModel.asComponent(this.model as IconModel), this.el);
  }
}
