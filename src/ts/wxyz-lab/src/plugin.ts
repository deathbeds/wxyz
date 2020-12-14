import { Application, IPlugin } from '@lumino/application';
import { Widget } from '@lumino/widgets';

import { IJupyterWidgetRegistry } from '@jupyter-widgets/base';

import { NAME, VERSION } from '.';
import '../style/index.css';

const EXTENSION_ID = `${NAME}:plugin`;

const plugin: IPlugin<Application<Widget>, void> = {
  id: EXTENSION_ID,
  requires: [IJupyterWidgetRegistry],
  autoStart: true,
  activate: (app: Application<Widget>, registry: IJupyterWidgetRegistry) => {
    registry.registerWidget({
      name: NAME,
      version: VERSION,
      exports: async () => {
        const widgetExports = await import('./widgets');
        (widgetExports.DockPopView as any)['app'] = app;
        return widgetExports;
      }
    });
  }
};

export default plugin;
