import marked from 'marked';

import {Model} from './base';


export class MarkdownModel extends Model {
  static model_name = 'MarkdownModel';

  defaults() {
    return {...super.defaults(),
      _model_name: MarkdownModel.model_name,
      value : '',
      source: '',
      error: ''
    };
  }

  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
    return this
      .on({
        'change:source': this.source_changed
      });
  }

  protected source_changed() {
    let changed = false;
    try {
      let value = marked.parse(this.get('source'));
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
