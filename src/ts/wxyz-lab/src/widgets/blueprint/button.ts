import * as React from 'react';
import * as ReactDOM from 'react-dom';

import {
  DOMWidgetView,
  DOMWidgetModel,
  unpack_models as deserialize
} from '@jupyter-widgets/base';

import { IconName } from '@blueprintjs/icons';
import { Button } from '@blueprintjs/core';

import { NAME, VERSION } from '../..';
import { IconModel } from './icon';

const h = React.createElement;

const BUTTON_CLASS = 'jp-WXYZ-Blueprint-Button';

export class ButtonModel extends DOMWidgetModel {
  static model_name = 'IconModel';
  static model_module = NAME;
  static model_module_version = VERSION;
  static view_name = 'IconView';
  static view_module = NAME;
  static view_module_version = VERSION;

  static serializers = {
    ...DOMWidgetModel.serializers,
    icon: { deserialize },
    icon_right: { deserialize }
  };

  get icon(): IconName | IconModel {
    return this.get('icon');
  }

  get rightIcon(): IconName | IconModel {
    return this.get('icon_right');
  }

  get text(): string {
    return this.get('description');
  }

  get disabled(): boolean {
    return this.get('disabled');
  }

  get large(): boolean {
    return this.get('large');
  }

  get loading(): boolean {
    return this.get('loading');
  }

  get minimal(): boolean {
    return this.get('minimal');
  }

  get small(): boolean {
    return this.get('small');
  }

  get active(): boolean {
    return this.get('active');
  }

  defaults() {
    return {
      ...super.defaults(),
      _model_name: ButtonModel.model_name,
      _model_module: NAME,
      _model_module_version: VERSION,
      _view_name: ButtonModel.view_name,
      _view_module: NAME,
      _view_module_version: VERSION,
      active: false,
      description: '',
      disabled: false,
      icon_right: null,
      icon: null,
      large: false,
      loading: false,
      minimal: false,
      small: false
    };
  }
}

export class ButtonView extends DOMWidgetView {
  private _iconHandlers = {} as any;

  render() {
    super.render();
    this.pWidget.addClass(BUTTON_CLASS);
    this.model.on('change', this.rerender, this);
    this._iconHandlers = {
      icon: this._iconHandler('icon'),
      icon_right: this._iconHandler('icon_right')
    };

    ['icon', 'icon_right'].forEach(attr => {
      const handler = this._iconHandler(attr);
      this.model.on(`change:${attr}`, handler, this);
      handler();
      this._iconHandlers[attr] = handler;
    });

    this.rerender();
  }

  _iconHandler(attr: string) {
    return () => {
      const prev = this.model.previous(attr);
      if (prev instanceof IconModel) {
        prev.off('change', this.rerender, this);
      }
      const current = this.model.get(attr);
      if (current instanceof IconModel) {
        current.on('change', this.rerender, this);
      }
    };
  }

  onClick = (event: any): void => {
    event.preventDefault();
    this.send({ event: 'click' });
  };

  get m() {
    return this.model as ButtonModel;
  }

  makeIcon(icon: IconName | IconModel | null) {
    if (!icon) {
      return;
    }

    if (typeof icon === 'string') {
      return IconModel.asComponent({
        icon,
        color: 'var(--jp-ui-font-color1)'
      } as IconModel);
    }

    return IconModel.asComponent(icon as IconModel);
  }

  rerender() {
    const { m, el, onClick } = this;

    ReactDOM.render(
      h(Button, {
        icon: this.makeIcon(m.icon),
        rightIcon: this.makeIcon(m.rightIcon),
        onClick,
        active: m.active,
        disabled: m.disabled,
        large: m.large,
        loading: m.loading,
        minimal: m.minimal,
        small: m.small,
        text: m.text
      }),
      el
    );
  }
}
