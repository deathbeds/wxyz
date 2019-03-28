import { BoxModel, BoxView } from '@jupyter-widgets/controls';

import { DataGrid, JSONModel } from '@phosphor/datagrid';

import { NAME, VERSION } from '..';

const CSS = {
  DATA_GRID: 'jp-WXYZ-DataGrid'
};

export class DataGridModel extends BoxModel {
  static model_name = 'DataGridModel';
  static model_module = NAME;
  static model_module_version = VERSION;
  static view_name: 'DataGridView';
  static view_module = NAME;
  static view_module_version = VERSION;

  defaults() {
    return {
      ...super.defaults(),
      _model_module: NAME,
      _model_module_version: VERSION,
      _view_module: NAME,
      _view_module_version: VERSION,
      _model_name: DataGridModel.model_name,
      _view_name: DataGridModel.view_name
    };
  }
}

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

class EventedDataGrid extends DataGrid {
  protected _view: DataGridView;
  protected _scrollLock = false;

  scrollTo(x: number, y: number): void {
    super.scrollTo(x, y);
    if (this._scrollLock) {
      return;
    }
    const m = this._view.model;
    const nx: number = (this as any)._scrollX;
    const ny: number = (this as any)._scrollY;
    const nmx: number = this.maxScrollX;
    const nmy: number = this.maxScrollY;
    const ox = m.get('scroll_x');
    const oy = m.get('scroll_y');
    if (ox === nx && oy === ny) {
      return;
    }
    this._view.model.set({
      scroll_x: nx,
      scroll_y: ny,
      max_x: nmx,
      max_y: nmy
    });
    this._view.touch();
  }

  get view() {
    return this._view;
  }

  set view(view: DataGridView) {
    const m = view.model;
    this._view = view;
    m.on('change:scroll_x change:scroll_y', this.onModelScroll, this);
    m.on(SIZES.map(t => `change:${t}`).join(' '), this.onModelSize, this);
    m.on(COLORS.map(t => `change:${t}`).join(' '), this.onColor, this);
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

  onModelScroll() {
    const m = this._view.model;
    let x = m.get('scroll_x');
    let y = m.get('scroll_y');
    if (x != null && y != null) {
      this._scrollLock = true;
      this.scrollTo(x, y);
      this._scrollLock = false;
    }
  }

  handleEvent(evt: Event) {
    super.handleEvent(evt);
    switch (evt.type) {
      default:
        break;
      case 'mousemove':
        this.updateHover(evt as MouseEvent);
        break;
    }
  }

  updateHover(evt: MouseEvent): void {
    const m = this._view.model;
    const { offsetX, offsetY } = evt as MouseEvent;
    const { headerWidth, headerHeight } = this;
    const r1 = (this as any)._rowSections.sectionIndex(
      offsetY - headerHeight + this.scrollY
    );
    const c1 = (this as any)._columnSections.sectionIndex(
      offsetX - headerWidth + this.scrollX
    );

    if (m.get('hover_row') === r1 && m.get('hover_column') === c1) {
      return;
    }

    m.set({
      hover_row: r1,
      hover_column: c1
    });

    this._view.touch();
  }
}

export class DataGridView extends BoxView {
  private _grid: EventedDataGrid;

  initialize(options: any) {
    super.initialize(options);
    this._grid = new EventedDataGrid();
    this._grid.view = this;
    this.model.on('change:value', this.onValue, this);
    this.pWidget.addWidget(this._grid);
    this.pWidget.addClass(CSS.DATA_GRID);
    this.onValue();
  }

  protected onValue() {
    const data = this.model.get('value');
    if (data) {
      this._grid.model = new JSONModel(data);
    } else {
      this._grid.model = null;
    }
  }
}
