import { Application, IPlugin } from '@phosphor/application';
import { Widget } from '@phosphor/widgets';

import { IJupyterWidgetRegistry, ExportData } from '@jupyter-widgets/base';

export function wxyzPlugin(
  opts: wxyzPlugin.IOptions
): IPlugin<Application<Widget>, void> {
  const EXTENSION_ID = `${opts.name}:plugin`;

  const plugin: IPlugin<Application<Widget>, void> = {
    id: EXTENSION_ID,
    requires: [IJupyterWidgetRegistry],
    autoStart: true,
    activate: (_: Application<Widget>, registry: IJupyterWidgetRegistry) => {
      registry.registerWidget(opts);
    }
  };

  return plugin;
}

export namespace wxyzPlugin {
  export interface IOptions {
    name: string;
    version: string;
    exports: ExportData;
    on?: IEventMap;
  }
  export interface IEventMap {
    register: (
      _: Application<Widget>,
      registry: IJupyterWidgetRegistry
    ) => void;
  }
}
