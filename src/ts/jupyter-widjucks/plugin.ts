import {Application, IPlugin} from '@phosphor/application';
import {Widget} from '@phosphor/widgets';

import {IJupyterWidgetRegistry} from '@jupyter-widgets/base';

import * as widgetExports from './widgets';
import * as V from './version';

const EXTENSION_ID = 'widjucks:plugin';

const plugin: IPlugin<Application<Widget>, void> = {
  id: EXTENSION_ID,
  requires: [IJupyterWidgetRegistry],
  autoStart: true,
  activate: (app: Application<Widget>, registry: IJupyterWidgetRegistry) => {
    registry.registerWidget({
      name: V.MODULE_NAME,
      version: V.MODULE_VERSION,
      exports: widgetExports,
    });
  }
};

export default plugin;
