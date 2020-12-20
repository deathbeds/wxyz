import { WXYZ } from '@deathbeds/wxyz-core/lib/widgets/_base';
import { unpack_models as deserialize } from '@jupyter-widgets/base';
import { DataGridModel, DataGridView } from './datagrid';
import { StyleGrid } from './pwidgets/stylegrid';
import { NAME, VERSION } from '..';

const CSS = {
  STYLE_GRID: 'jp-WXYZ-StyleGrid',
};

/** A DataGrid Style for simple styles (e.g. JSON-compatible)
 */
export class GridStyleModel extends WXYZ {
  static model_module = NAME;
  static model_module_version = VERSION;
  static model_name = 'GridStyleModel';

  defaults() {
    return {
      ...super.defaults(),
      _model_name: GridStyleModel.model_name,
      _model_module: NAME,
      _model_module_version: VERSION,
    };
  }
}

export class StyleGridModel extends DataGridModel {
  static model_name = 'StyleGridModel';
  static view_name = 'StyleGridView';

  static serializers = {
    ...DataGridModel.serializers,
    grid_style: { deserialize },
  };

  defaults() {
    return {
      ...super.defaults(),
      _model_name: StyleGridModel.model_name,
      _view_name: StyleGridModel.view_name,
      grid_style: null as GridStyleModel,
      header_visibility: 'all',
    };
  }
}

export class StyleGridView extends DataGridView {
  model: StyleGridModel;

  protected createGrid() {
    return new StyleGrid();
  }

  initialize(options: any) {
    options.createGrid = () => this.createGrid();
    super.initialize(options);
    this.pWidget.addClass(CSS.STYLE_GRID);
  }
}
