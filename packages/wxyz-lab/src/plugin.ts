import { Application, IPlugin } from '@lumino/application';
import { Widget } from '@lumino/widgets';

import { IRenderMimeRegistry } from '@jupyterlab/rendermime';

import { IJupyterWidgetRegistry } from '@jupyter-widgets/base';

import '../style/index.css';

import { NAME, VERSION } from './constants';

const EXTENSION_ID = `${NAME}:plugin`;

const plugin: IPlugin<Application<Widget>, void> = {
  id: EXTENSION_ID,
  requires: [IJupyterWidgetRegistry],
  optional: [IRenderMimeRegistry],
  autoStart: true,
  activate: (
    app: Application<Widget>,
    registry: IJupyterWidgetRegistry,
    mimeRegistry?: IRenderMimeRegistry
  ) => {
    registry.registerWidget({
      name: NAME,
      version: VERSION,
      exports: async () => {
        const widgetExports = await import('./widgets');
        (widgetExports.DockPopView as any)['app'] = app;
        widgetExports.MarkdownModel.mimeRegistry = mimeRegistry;
        return widgetExports;
      },
    });
  },
};

export default plugin;
