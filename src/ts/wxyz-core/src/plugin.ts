import { NAME as name, VERSION as version } from '.';
import { wxyzPlugin } from './util';
import * as exports from './widgets';
import '../style/index.css';

const plugin = wxyzPlugin({ name, version, exports });
export default plugin;
