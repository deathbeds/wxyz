import { PromiseDelegate } from '@lumino/coreutils';

import { renderMarkdown } from '@jupyterlab/rendermime';
import { IRenderMimeRegistry } from '@jupyterlab/rendermime';

import { FnModel } from '@deathbeds/wxyz-core';

export class MarkdownModel extends FnModel<string, string, MarkdownModel.ITraits> {
  static model_name = 'MarkdownModel';

  defaults() {
    return {
      ...super.defaults(),
      _model_name: MarkdownModel.model_name,
    };
  }

  async theFunction(source: string) {
    const value = await Private.render(source);
    return value;
  }
}

export namespace MarkdownModel {
  export interface ITraits extends FnModel.ITraits<string, string> {}
  export let mimeRegistry: IRenderMimeRegistry | null;
}

namespace Private {
  let _iframe: HTMLIFrameElement | null = null;
  let _ready: PromiseDelegate<void> | null = null;

  async function ensureFrame(): Promise<void> {
    return new Promise((resolve) => {
      _iframe = document.createElement('iframe');
      _iframe.id = 'jp-wxyz-markdown-iframe';
      _iframe.onload = () => {
        _ready.resolve();
        resolve();
      };
      document.body.appendChild(_iframe);
      _iframe.src = 'about:blank';
    });
  }

  export async function render(source: string): Promise<string> {
    if (_ready == null) {
      _ready = new PromiseDelegate();
      await ensureFrame();
    }
    await _ready.promise;
    const { mimeRegistry } = MarkdownModel;
    const { contentDocument } = _iframe;

    const host = contentDocument.createElement('div');

    contentDocument.body.appendChild(host);

    try {
      await renderMarkdown({
        source,
        host,
        trusted: true,
        shouldTypeset: false,
        resolver: mimeRegistry?.resolver,
        linkHandler: mimeRegistry?.linkHandler,
        latexTypesetter: null,
        sanitizer: mimeRegistry?.sanitizer,
      });
      return host.innerHTML;
    } finally {
      contentDocument.body.removeChild(host);
    }
  }
}
