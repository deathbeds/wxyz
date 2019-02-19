import * as nunjucks from 'nunjucks';

import {WidgetModel} from '@jupyter-widgets/base';

import {Model} from './base';

nunjucks.installJinjaCompat();


export class TemplateModel extends Model {
  static model_name = 'TemplateModel';

  private _env = new nunjucks.Environment();
  private _template: nunjucks.Template = nunjucks.compile('');

  defaults() {
    return {...super.defaults(),
      _model_name: TemplateModel.model_name,
      value : '',
      template: '',
      context: null,
      error: ''
    };
  }

  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
    this
      .on({
        'change:template': this.template_changed,
        'change:context': this.context_changed
      })
      .template_changed()
      .update_value();
    return this;
  }

  protected context_changed() {
    console.log(this.get('context'));
  }

  protected template_changed() {
    try {
      this._template = nunjucks.compile(this.get('template') || '', this._env);
    } catch(err) {
      this.set('error', `${err}`);
    }
    return this;
  }

  protected update_value() {
    let changed = false;
    let contextWidget: WidgetModel = this.get('context');

    let context = contextWidget ? contextWidget.attributes : {};

    try {
      let value = this._template.render(context);
      if (value !== this.get('value')) {
        this.set('value', value);
        changed = true;
      }
      this.set('error', '');
    } catch(err) {
      this.set('err', `${err}`);
      changed = true;
    } finally {
      changed && this.save();
    }
    return this;
  }
}
