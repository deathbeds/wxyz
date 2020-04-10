import { JSONModel, DataModel } from '@lumino/datagrid';
import { WidgetModel } from '@jupyter-widgets/base';

export class WXYZJSONModel extends JSONModel {
  jmodel: WidgetModel;

  metadata(region: DataModel.CellRegion, column: number) {
    return {
      jmodel: this.jmodel.attributes,
      ...super.metadata(region, column)
    };
  }
}
