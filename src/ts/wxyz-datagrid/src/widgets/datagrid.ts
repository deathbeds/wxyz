import { BoxView } from '@jupyter-widgets/controls';

import { DataGrid } from '@lumino/datagrid';

import { unpack_models as deserialize } from '@jupyter-widgets/base';

import { WXYZBox } from '@deathbeds/wxyz-core/lib/widgets/_base';
import { WXYZJSONModel } from './pmodels/jsonmodel';

const CSS = {
  DATA_GRID: 'jp-WXYZ-DataGrid'
};

export class DataGridModel extends WXYZBox {
  static model_name = 'DataGridModel';
  static view_name = 'DataGridView';

  static serializers = {
    ...WXYZBox.serializers,
    cell_renderers: { deserialize }
  };

  defaults() {
    return {
      ...super.defaults(),
      _model_name: DataGridModel.model_name,
      _view_name: DataGridModel.view_name
    };
  }
}

export class DataGridView extends BoxView {
  protected _grid: DataGridView.IViewedGrid;

  initialize(options: DataGridView.IOptions) {
    const createGrid = options.createGrid || this.createGrid;
    super.initialize(options);
    this._grid = createGrid();
    this._grid.view = this;
    this.model.on('change:value', this.onValue, this);
    this.pWidget.addWidget(this._grid);
    this.pWidget.addClass(CSS.DATA_GRID);
    this.onValue();
  }

  protected createGrid(): DataGridView.IViewedGrid {
    return new DataGrid() as DataGridView.IViewedGrid;
  }

  protected onValue() {
    const data = this.model.get('value');
    if (data) {
      this._grid.model = new WXYZJSONModel(data);
      (this._grid.model as any).jmodel = this.model;
    } else {
      this._grid.model = null;
    }
    this._grid.repaint();
  }
}

export namespace DataGridView {
  export interface IViewedGrid extends DataGrid {
    view: DataGridView;
  }
  export interface IOptions {
    createGrid: () => IViewedGrid;
  }
}
