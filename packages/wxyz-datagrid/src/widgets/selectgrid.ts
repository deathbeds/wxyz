import { toArray } from '@lumino/algorithm';
import { JSONExt } from '@lumino/coreutils';
import { BasicSelectionModel } from '@lumino/datagrid';

import { unpack_models as deserialize } from '@jupyter-widgets/base';

import { SelectGrid } from './pwidgets/selectgrid';
import { StyleGridModel, StyleGridView } from './stylegrid';

const CSS = {
  SELECT_GRID: 'jp-WXYZ-SelectGrid',
};

export type TSelection = [number, number, number, number];

export class SelectGridModel extends StyleGridModel {
  static model_name = 'SelectGridModel';
  static view_name = 'SelectGridView';

  static serializers = {
    ...StyleGridModel.serializers,
    selection: { deserialize },
  };

  protected createGrid() {
    return new SelectGrid();
  }

  defaults() {
    return {
      ...super.defaults(),
      _model_name: SelectGridModel.model_name,
      _view_name: SelectGridModel.view_name,
    };
  }
}

export class SelectGridView extends StyleGridView {
  model: SelectGridModel;

  protected isUpdatingSelections = false;

  createGrid() {
    return new SelectGrid();
  }

  initialize(options: any) {
    options.createGrid = () => this.createGrid();
    super.initialize(options);
    this.luminoWidget.addClass(CSS.SELECT_GRID);
    this.model.on('change:selections', this.onModelSelectionsChanged, this);
  }

  protected onValue() {
    if (this._grid.selectionModel) {
      this._grid.selectionModel.changed.disconnect(this.onGridSelectionChanged, this);
    }
    super.onValue();

    const { dataModel } = this._grid;
    if (dataModel != null) {
      const selectionModel = new BasicSelectionModel({ dataModel });
      this._grid.selectionModel = selectionModel;
      this._grid.selectionModel.changed.connect(this.onGridSelectionChanged, this);
    }
  }

  protected onModelSelectionsChanged() {
    const mSelections: TSelection[] = this.model.get('selections');
    const gSelections = this.gridSelectionToModel();
    const { selectionModel } = this._grid;

    if (selectionModel == null || JSONExt.deepEqual(mSelections, gSelections)) {
      return;
    }

    this.isUpdatingSelections = true;
    selectionModel.clear();

    for (const selection of mSelections) {
      const [c1, c2, r1, r2] = selection;
      selectionModel.select({
        c1,
        c2,
        r1,
        r2,
        cursorColumn: Math.min(c1, c2),
        cursorRow: Math.min(r1, r2),
        clear: 'none',
      });
    }

    this.isUpdatingSelections = false;
  }

  protected gridSelectionToModel() {
    const { selectionModel } = this._grid;
    let selections: TSelection[] = [];
    for (const selection of toArray(selectionModel.selections())) {
      const { c1, c2, r1, r2 } = selection;
      selections.push([c1, c2, r1, r2]);
    }
    return selections;
  }

  onGridSelectionChanged() {
    if (this.isUpdatingSelections) {
      return;
    }

    const { selectionModel } = this._grid;

    const mSelections = this.model.get('selections');

    let gSelections: TSelection[];

    if (selectionModel != null) {
      gSelections = this.gridSelectionToModel();
    }

    if (JSONExt.deepEqual(mSelections, gSelections)) {
      return;
    }

    this.model.set({ selections: gSelections });
    this.touch();
  }
}
