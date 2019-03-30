import { unpack_models as deserialize } from '@jupyter-widgets/base';
import { DataGridModel, DataGridView } from './datagrid';
import { StyleGrid } from './pwidgets/stylegrid';

const CSS = {
  STYLE_GRID: 'jp-WXYZ-StyleGrid'
};

export class StyleGridModel extends DataGridModel {
  static model_name = 'StyleGridModel';
  static view_name = 'StyleGridView';

  static serializers = {
    ...DataGridModel.serializers,
    selection: { deserialize }
  };

  defaults() {
    return {
      ...super.defaults(),
      _model_name: StyleGridModel.model_name,
      _view_name: StyleGridModel.view_name
    };
  }
}

export class StyleGridView extends DataGridView {
  protected createGrid() {
    return new StyleGrid();
  }

  initialize(options: any) {
    options.createGrid = () => this.createGrid();
    super.initialize(options);
    this.pWidget.addClass(CSS.STYLE_GRID);
  }
}
