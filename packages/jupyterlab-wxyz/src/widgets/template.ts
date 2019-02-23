import * as nunjucks from 'nunjucks';

import {
  WidgetModel,
  unpack_models as deserialize
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
      context: null as WidgetModel
    };
  }

  async theFunction(source: string) {
    let context = this.theContext;
    if (context instanceof WidgetModel) {
      context = context.attributes;
    }
    let promise = new Promise<string>((resolve, reject) => {
      return nunjucks.renderString(source || '', context || {}, (err, res) => {
        if (err) {
          reject(err);
          return;
        } else {
          resolve(res);
        }
      });
    });
    return await promise;
  }

  get theContext() {
    return this.get('context');
  }
  set theContext(context: TemplateModel.TContext) {
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
    let previous = (this.previousAttributes() as any).context;
    if (previous instanceof WidgetModel) {
      previous.off(void 0, void 0, this);
    }
    let context = this.theContext;
    if (context instanceof WidgetModel) {
      context.on('change', this.theSourceChanged, this);
    }
    this.theSourceChanged();
  }
}

export namespace TemplateModel {
  export type TContext = WidgetModel | object | Array<any> | null;
  export interface ITraits extends FnModel.ITraits<string, string> {
    context: TContext;
  }
}
