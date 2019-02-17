// Copyright (c) dead pixels collective
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel, DOMWidgetView, ISerializers
} from '@jupyter-widgets/base';

import { defaultSanitizer } from '@jupyterlab/apputils';

import * as renderers from '@jupyterlab/rendermime';

import * as nunjucks from 'nunjucks';

import * as marked from 'marked';

nunjucks.installJinjaCompat();

import {
  MODULE_NAME, MODULE_VERSION
} from './version';


export
class WidjuckModel extends DOMWidgetModel {
  private env = new nunjucks.Environment();

  defaults() {
    return {...super.defaults(),
      _model_name: WidjuckModel.model_name,
      _model_module: WidjuckModel.model_module,
      _model_module_version: WidjuckModel.model_module_version,
      _view_name: WidjuckModel.view_name,
      _view_module: WidjuckModel.view_module,
      _view_module_version: WidjuckModel.view_module_version,
      value : '',
      template: ''
    };
  }

  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
    this.on('change:template', this._template_changed, this);
    this.on('change', this._template_context_changed, this);
    this._template_changed();
  }

  private _template_changed() {
    try {
      this._template = nunjucks.compile(this.get('template') || '', this.env);
      this._template_context_changed();
    } catch(err) {
      console.error(err);
    }
  }

  private _template_context_changed() {
    let oldHTML = this.get('value');
    try {
      const html = marked.parse(this._template.render({
        ...this.attributes,
        value: null
      }));
      if (oldHTML !== html) {
        this.set('value', html);
        this.save();
      }
    } catch(err) {
      console.error(err);
    }
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  }

  private _template: nunjucks.Template = nunjucks.compile('');

  static model_name = 'WidjuckModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'WidjuckView';   // Set to null if no view
  static view_module = MODULE_NAME;   // Set to null if no view
  static view_module_version = MODULE_VERSION;
}


export
class WidjuckView extends DOMWidgetView {
  render() {
    this.value_changed();
    this.model.on('change:value', this.value_changed, this);
  }

  value_changed() {
    renderers.renderHTML({
      host: this.el,
      source: this.model.get('value'),
      trusted: true,
      sanitizer: defaultSanitizer,
      resolver: null,
      linkHandler: null,
      shouldTypeset: false,
      latexTypesetter: null
    });
  }
}
