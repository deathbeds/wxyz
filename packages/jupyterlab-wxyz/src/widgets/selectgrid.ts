import { unpack_models as deserialize } from '@jupyter-widgets/base';
import { DataGridModel, DataGridView } from './datagrid';
import { SelectGrid } from './pwidgets/selectgrid';

const CSS = {
  SELECT_GRID: 'jp-WXYZ-SelectGrid'
};

export class SelectGridModel extends DataGridModel {
  static model_name = 'SelectGridModel';
  static view_name = 'SelectGridView';

  static serializers = {
    ...DataGridModel.serializers,
    selection: { deserialize }
  };

  protected createGrid() {
    return new SelectGrid();
  }

  defaults() {
    return {
      ...super.defaults(),
      _model_name: SelectGridModel.model_name,
      _view_name: SelectGridModel.view_name
    };
  }
}

export class SelectGridView extends DataGridView {
  createGrid() {
    return new SelectGrid();
  }

  initialize(options: any) {
    options.createGrid = () => this.createGrid();
    super.initialize(options);
    this.pWidget.addClass(CSS.SELECT_GRID);
  }
}
