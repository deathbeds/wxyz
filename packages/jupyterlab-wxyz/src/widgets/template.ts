import * as nunjucks from 'nunjucks';

import {
  WidgetModel,
  unpack_models as deserialize,
} from '@jupyter-widgets/base';

import { FnModel } from './base';

nunjucks.installJinjaCompat();

export class TemplateModel extends FnModel<
  string,
  string,
  TemplateModel.ITraits
> {
  static model_name = 'TemplateModel';
  static serializers = { ...FnModel.serializers, context: { deserialize } };

  defaults() {
    return {
      ...super.defaults(),
      _model_name: TemplateModel.model_name,
      context: null,
    };
  }

  theFunction(source: string) {
    let context = (this.theContext || {}).attributes || {};
    return nunjucks.renderString(source || '', context);
  }

  get theContext() {
    return this.get('context');
  }
  set theContext(context: WidgetModel) {
    this.set('context', context);
    this.save();
  }

  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
    this.on('change:context', this.theContextChanged, this);
    this.theContextChanged();
    this.theSourceChanged();
    return this;
  }

  protected theContextChanged(): void {
    let previous = (this.previousAttributes() as any).context as WidgetModel;
    previous && previous.off && previous.off(void 0, void 0, this);
    this.theContext &&
      this.theContext.on &&
      this.theContext.on('change', this.theSourceChanged, this);
    this.theSourceChanged();
  }
}

export namespace TemplateModel {
  export interface ITraits extends FnModel.ITraits<string, string> {
    context: WidgetModel | null;
  }
}
