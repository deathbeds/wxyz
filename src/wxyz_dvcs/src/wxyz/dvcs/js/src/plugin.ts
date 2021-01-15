import { Application, IPlugin } from '@lumino/application';
import { Widget } from '@lumino/widgets';

import { IJupyterWidgetRegistry } from '@jupyter-widgets/base';

import { NAME, VERSION } from './constants';
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
      exports: () => import('./widgets'),
    });
  },
};

export default plugin;
