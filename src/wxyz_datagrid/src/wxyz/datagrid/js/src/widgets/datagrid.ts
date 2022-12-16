import { BasicKeyHandler, BasicMouseHandler, DataGrid } from '@lumino/datagrid';

import { unpack_models as deserialize } from '@jupyter-widgets/base';
import { BoxView } from '@jupyter-widgets/controls';

import { WXYZBox } from '@deathbeds/wxyz-core';

import { WXYZJSONModel } from './pmodels/jsonmodel';

const CSS = {
  DATA_GRID: 'jp-WXYZ-DataGrid',
};

export class DataGridModel extends WXYZBox {
  static model_name = 'DataGridModel';
  static view_name = 'DataGridView';

  static serializers = {
    ...WXYZBox.serializers,
    cell_renderers: { deserialize },
  };

  defaults() {
    return {
      ...super.defaults(),
      _model_name: DataGridModel.model_name,
      _view_name: DataGridModel.view_name,
    };
  }
}

export class DataGridView extends BoxView {
  protected _grid: DataGridView.IViewedGrid;

  initialize(options: DataGridView.IOptions) {
    super.initialize(options);
    const createGrid = options.createGrid || this.createGrid;
    super.initialize(options);
    this._grid = createGrid();
    this.addGridBehaviors(this._grid);
    this._grid.view = this;
    this.model.on('change:value', this.onValue, this);
    this.luminoWidget.addWidget(this._grid);
    this.luminoWidget.addClass(CSS.DATA_GRID);
    this.onValue();
  }

  protected createGrid(): DataGridView.IViewedGrid {
    return new DataGrid() as DataGridView.IViewedGrid;
  }

  protected addGridBehaviors(grid: DataGridView.IViewedGrid) {
    grid.keyHandler = new BasicKeyHandler();
    grid.mouseHandler = new BasicMouseHandler();
  }

  protected onValue() {
    const data = this.model.get('value');
    if (data) {
      this._grid.dataModel = new WXYZJSONModel(data);
      (this._grid.dataModel as any).jmodel = this.model;
    } else {
      this._grid.dataModel = null;
    }
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
