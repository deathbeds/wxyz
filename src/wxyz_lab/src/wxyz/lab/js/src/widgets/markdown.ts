// no need to lazy load marked, as it's already in vendoer~main
import marked from 'marked';

import { FnModel } from '@deathbeds/wxyz-core/lib/widgets/_base';

export class MarkdownModel extends FnModel<
  string,
  string,
  MarkdownModel.ITraits
> {
  static model_name = 'MarkdownModel';

  defaults() {
    return {
      ...super.defaults(),
      _model_name: MarkdownModel.model_name,
    };
  }

  async theFunction(source: string) {
    const promise = new Promise<string>((resolve, reject) => {
      marked.parse(source, {}, (err, result) => {
        if (err) {
          reject(err);
          return;
        }
        resolve(result);
      });
    });
    return await promise;
  }
}

export namespace MarkdownModel {
  export interface ITraits extends FnModel.ITraits<string, string> {}
}
