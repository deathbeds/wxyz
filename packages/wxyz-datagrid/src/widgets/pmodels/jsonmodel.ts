import { DataModel, JSONModel } from '@lumino/datagrid';

import { WidgetModel } from '@jupyter-widgets/base';

export class WXYZJSONModel extends JSONModel {
  jmodel: WidgetModel;

  metadata(region: DataModel.CellRegion, row: number, column: number) {
    return {
      jmodel: this.jmodel?.attributes,
      ...super.metadata(region, row, column),
    };
  }
}
