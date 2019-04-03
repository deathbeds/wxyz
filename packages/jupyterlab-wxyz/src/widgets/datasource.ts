import { WXYZ } from './_base';
import { WXYZJSONModel } from './pmodels/jsonmodel';
import { WXYZNDArrayModel } from './pmodels/ndarraymodel';
import { DataModel } from '@phosphor/datagrid';

import { listenToUnion } from 'jupyter-dataserializers';

export class DataSourceModel extends WXYZ {
  static model_name = 'DataSourceModel';

  gridModel(): DataModel {
    return null;
  }

  defaults() {
    return {
      ...super.defaults(),
      _model_name: DataSourceModel.model_name
    };
  }
}

export class TableSchemaSourceModel extends DataSourceModel {
  static model_name = 'TableSchemaSourceModel';

  gridModel(): DataModel {
    return new WXYZJSONModel(this.get('value'));
  }

  defaults() {
    return {
      ...super.defaults(),
      _model_name: TableSchemaSourceModel.model_name
    };
  }
}

export class NDArraySourceModel extends DataSourceModel {
  static model_name = 'NDArraySourceModel';

  gridModel(): DataModel {
    let model = new WXYZNDArrayModel(this.get('value'));

    listenToUnion(this, 'value', (...args: any[]) => {
      console.log('changed', args, model);
    });
    return model;
  }

  defaults() {
    return {
      ...super.defaults(),
      _model_name: NDArraySourceModel.model_name
    };
  }
}
