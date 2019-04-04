import { WXYZ } from './_base';
import { PWXYZJSONModel } from './pmodels/jsonmodel';
import { PWXYZNDArrayModel } from './pmodels/ndarraymodel';
import { DataModel } from '@phosphor/datagrid';

import {
  data_union_serialization // ,
  // listenToUnion
} from 'jupyter-dataserializers';

export class WXYZDataSourceModel extends WXYZ {
  static model_name = 'WXYZDataSourceModel';

  gridModel(): DataModel {
    return null;
  }

  defaults() {
    return {
      ...super.defaults(),
      _model_name: WXYZDataSourceModel.model_name
    };
  }
}

export class WXYZTableSchemaModel extends WXYZDataSourceModel {
  static model_name = 'WXYZTableSchemaModel';

  gridModel(): DataModel {
    return new PWXYZJSONModel(this.get('value'));
  }

  defaults() {
    return {
      ...super.defaults(),
      _model_name: WXYZTableSchemaModel.model_name
    };
  }
}

export class WXYZNDArrayModel extends WXYZDataSourceModel {
  static model_name = 'WXYZNDArrayModel';
  private _gridModel: PWXYZNDArrayModel;

  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
    this.on('change:value', () => {
      this._gridModel.setNDArray(this.get('value'));
    });
  }

  gridModel(): DataModel {
    if (!this._gridModel) {
      this._gridModel = new PWXYZNDArrayModel(this.get('value'));
    }
    return this._gridModel;
  }

  static serializers = {
    ...WXYZDataSourceModel.serializers,
    value: data_union_serialization
  };

  defaults() {
    return {
      ...super.defaults(),
      _model_name: WXYZNDArrayModel.model_name
    };
  }
}
