import { DataGrid } from '@lumino/datagrid';

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
    // this.cellRenderers.set(
    //   rm.get('region') || 'body',
    //   rm.get('metadata') || {},
    //   rm.toRenderer(() => this.setRenderer(rm))
    // );
  }

  makeRenderers() {
    let rms: CellRendererModel[] = this._view.model.get('cell_renderers');
    return rms.map(rm => {
      return {
        region: rm.get('region') || 'body',
        metadata: rm.get('metadata') || {},
        renderer: rm.toRenderer(() => this.setRenderer(rm)),
        model: rm
      };
    });
  }

  onModelCellRenderers() {
    // this.cellRenderers.clear();
    // let renderers = this.makeRenderers();
    // renderers.map(r => {
    //   if (r.model) {
    //     r.model.on('change', () => this.setRenderer(r.model));
    //   }
    //   this.cellRenderers.set(r.region, r.metadata, r.renderer);
    // });
    // this.repaint();
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
    // const m = this._view.model;
    // const changed = Object.keys(m.changedAttributes());
    // for (const size of changed) {
    //   let v = m.get(size);
    //   if (v == null) {
    //     continue;
    //   }
    //   switch (size) {
    //     default:
    //       continue;
    //     case 'row_size':
    //       this.baseRowSize = v;
    //       continue;
    //     case 'row_header_size':
    //       this.baseRowHeaderSize = v;
    //       continue;
    //     case 'column_size':
    //       this.baseColumnSize = v;
    //       continue;
    //     case 'column_header_size':
    //       this.baseColumnHeaderSize = v;
    //       continue;
    //   }
    // }
  }
}
