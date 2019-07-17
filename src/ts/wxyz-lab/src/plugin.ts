import { NAME as name, VERSION as version } from '.';
import { wxyzPlugin } from '@deathbeds/wxyz-core/lib/util';
import * as exports from './widgets';
import '../style/index.css';

const plugin = wxyzPlugin({
  name,
  version,
  exports,
  on: {
    register: (app, _registry) => {
      (exports.DockPopView as any)['app'] = app;
    }
  }
});

export default plugin;
