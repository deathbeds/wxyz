import { DataModel } from '@phosphor/datagrid';

import { getArray } from 'jupyter-dataserializers';

// import ndarray from 'ndarray';

export class WXYZNDArrayModel extends DataModel {
  private _data: any;

  constructor(data: any) {
    super();
    this._data = data;
  }

  columnCount(region: DataModel.ColumnRegion) {
    return region === 'body' ? this._data.shape[1] : 1;
  }

  rowCount(region: DataModel.RowRegion): number {
    return region === 'body' ? this._data.shape[0] : 1;
  }

  data(region: DataModel.CellRegion, row: number, column: number) {
    try {
      console.log('woo');
      const array = getArray(this._data);
      console.log(array.get(row, column));
    } catch (err) {
      console.log('whoops', err);
    }
    return region + row + column;
  }
}
