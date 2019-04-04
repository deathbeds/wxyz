import { JSONModel, DataModel } from '@phosphor/datagrid';
import { WidgetModel } from '@jupyter-widgets/base';

export class PWXYZJSONModel extends JSONModel {
  jmodel: WidgetModel;

  metadata(region: DataModel.CellRegion, column: number) {
    return {
      jmodel: this.jmodel.attributes,
      ...super.metadata(region, column)
    };
  }
}
