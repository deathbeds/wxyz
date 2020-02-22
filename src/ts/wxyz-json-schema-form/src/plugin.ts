import { Application, IPlugin } from '@phosphor/application';
import { Widget } from '@phosphor/widgets';

import { IJupyterWidgetRegistry } from '@jupyter-widgets/base';

import { NAME, VERSION } from '.';
import '../style/index.css';

const EXTENSION_ID = `${NAME}:plugin`;

const plugin: IPlugin<Application<Widget>, void> = {
  id: EXTENSION_ID,
  requires: [IJupyterWidgetRegistry],
  autoStart: true,
  activate: (_: Application<Widget>, registry: IJupyterWidgetRegistry) => {
    registry.registerWidget({
      name: NAME,
      version: VERSION,
      exports: async () => import('./widgets')
    });
  }
};

export default plugin;
