import { DataModel } from '@phosphor/datagrid';

import ndarray from 'ndarray';

export class PWXYZNDArrayModel extends DataModel {
  private _data: ndarray;

  constructor(data: ndarray) {
    super();
    this._data = data;
  }

  columnCount(region: DataModel.ColumnRegion) {
    return region === 'body' ? this._data.shape[1] : 1;
  }

  rowCount(region: DataModel.RowRegion): number {
    return region === 'body' ? this._data.shape[0] : 1;
  }

  setNDArray(data: ndarray) {
    this._data = data;
    this.emitChanged({ type: 'model-reset' });
  }

  data(region: DataModel.CellRegion, row: number, column: number) {
    switch (region) {
      case 'body':
        return this._data.get(row, column);
      case 'row-header':
        return row;
      case 'column-header':
        return column;
      case 'corner-header':
        return this._data.shape.map(String).join('×');
      default:
        return region;
    }
  }
}
