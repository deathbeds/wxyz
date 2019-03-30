import { DataGrid, TextRenderer, CellRenderer } from '@phosphor/datagrid';

// TODO: fix circulare references
import { DataGridView } from '../datagrid';
import { CellRendererModel } from '../models/cells';

const SIZES = [
  'row_size',
  'column_size',
  'row_header_size',
  'column_header_size'
];

const COLORS = [
  'void_color',
  'background_color',
  'grid_line_color',
  'header_background_color',
  'header_grid_line_color'
];

const SELECTED: CellRenderer.ConfigFunc<string> = config => {
  let selection: number[] = null;
  try {
    selection = (config.metadata as any).jmodel.selection;
  } catch {
    // whatever
  }

  if (
    selection &&
    config.column >= selection[0] &&
    config.column <= selection[1] &&
    config.row >= selection[2] &&
    config.row <= selection[3]
  ) {
    return 'rgba(0,0,255,0.125)';
  }
  return 'rgba(0,0,0,0)';
};

export class StyleGrid extends DataGrid implements DataGridView.IViewedGrid {
  protected _view: DataGridView;

  get view() {
    return this._view;
  }

  set view(view: DataGridView) {
    this._view = view;
    this.onSetView();
  }

  protected onSetView() {
    const m = this.view.model;
    m.on('change:cell_renderers', this.onModelCellRenderers, this);
    m.on(SIZES.map(t => `change:${t}`).join(' '), this.onModelSize, this);
    m.on(COLORS.map(t => `change:${t}`).join(' '), this.onColor, this);
    this.onModelCellRenderers();
    this.onModelSize();
    this.onColor();
  }

  setRenderer(rm: CellRendererModel) {
    this.cellRenderers.set(
      rm.get('region') || 'body',
      rm.get('metadata') || {},
      rm.toRenderer(() => this.setRenderer(rm))
    );
  }

  onModelCellRenderers() {
    let renderers: CellRendererModel[] = this._view.model.get('cell_renderers');

    this.cellRenderers.clear();

    this.cellRenderers.set(
      'body',
      {},
      new TextRenderer({ backgroundColor: SELECTED })
    );

    for (let rm of renderers) {
      rm.on('change', () => this.setRenderer(rm));
      this.setRenderer(rm);
    }
  }

  onColor() {
    const m = this._view.model;
    const changed = Object.keys(m.changedAttributes());
    let style = {} as any;
    for (const color of changed) {
      let v = m.get(color);
      if (v == null) {
        continue;
      }

      switch (color) {
        default:
          continue;
        case 'void_color':
          style.voidColor = v;
          break;
        case 'background_color':
          style.backgroundColor = v;
          break;
        case 'grid_line_color':
          style.gridLineColor = v;
          break;
        case 'header_background_color':
          style.headerBackgroundColor = v;
          break;
        case 'header_grid_line_color':
          style.headerGridLineColor = v;
          break;
      }
      this.style = { ...this.style, ...style };
    }
  }

  onModelSize() {
    const m = this._view.model;
    const changed = Object.keys(m.changedAttributes());
    for (const size of changed) {
      let v = m.get(size);
      if (v == null) {
        continue;
      }
      switch (size) {
        default:
          continue;
        case 'row_size':
          this.baseRowSize = v;
          continue;
        case 'row_header_size':
          this.baseRowHeaderSize = v;
          continue;
        case 'column_size':
          this.baseColumnSize = v;
          continue;
        case 'column_header_size':
          this.baseColumnHeaderSize = v;
          continue;
      }
    }
  }
}
