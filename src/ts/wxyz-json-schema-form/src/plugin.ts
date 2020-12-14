import { Application, IPlugin } from '@lumino/application';
import { Widget } from '@lumino/widgets';

import { IJupyterWidgetRegistry } from '@jupyter-widgets/base';

import { NAME, VERSION } from '.';

import { IRenderMimeRegistry } from '@jupyterlab/rendermime';

import '../style/index.css';

const EXTENSION_ID = `${NAME}:plugin`;

const plugin: IPlugin<Application<Widget>, void> = {
  id: EXTENSION_ID,
  requires: [IJupyterWidgetRegistry],
  optional: [IRenderMimeRegistry],
  autoStart: true,
  activate: (
    _: Application<Widget>,
    registry: IJupyterWidgetRegistry,
    rendermime: IRenderMimeRegistry
  ) => {
    registry.registerWidget({
      name: NAME,
      version: VERSION,
      exports: async () => {
        const widgetExports = import('./widgets');
        // TODO: restore
        // (await widgetExports).JSONSchemaFormView._rendermime = rendermime;
        return widgetExports;
      }
    });
  }
};

export default plugin;
