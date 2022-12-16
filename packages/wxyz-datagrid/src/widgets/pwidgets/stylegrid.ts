import { DataGrid } from '@lumino/datagrid';

// TODO: fix circular references
import { DataGridView } from '../datagrid';
import { CellRendererModel } from '../models/cells';

import { GridStyleModel } from '..';

interface IHasChanged {
  changed: { [key: string]: any };
}

const SIZES = ['row_size', 'column_size', 'row_header_size', 'column_header_size'];

const WATCHED_STYLES = [
  // the part between these comments will be rewritten
  // BEGIN SCHEMAGEN:PROPERTIES IDataGridStyles @b911858621aef508319fec6b6d1cbe8afeeb8ffafe0646c0083d9491e3277e78
  'backgroundColor',
  'columnBackgroundColor',
  'cursorBorderColor',
  'cursorFillColor',
  'gridLineColor',
  'headerBackgroundColor',
  'headerGridLineColor',
  'headerHorizontalGridLineColor',
  'headerSelectionBorderColor',
  'headerSelectionFillColor',
  'headerVerticalGridLineColor',
  'horizontalGridLineColor',
  'rowBackgroundColor',
  'scrollShadow',
  'selectionBorderColor',
  'selectionFillColor',
  'verticalGridLineColor',
  'voidColor',
  // END SCHEMAGEN:PROPERTIES
];

const STYLE_EVENTS = WATCHED_STYLES.reduce((m, o) => `${m} change:${o}`, '');

const DEFAULT_COLOR = 'rgba(0,0,0,0.0)';

export class StyleGrid extends DataGrid implements DataGridView.IViewedGrid {
  protected _view: DataGridView;

  get view() {
    return this._view;
  }

  set view(view: DataGridView) {
    this._view = view;
    this.onSetView();
  }

  styleFunctor(values: string[]) {
    const len = values.length;
    return (i: number) => {
      if (len == 0) {
        return DEFAULT_COLOR;
      }
      return (i < len ? values[i] : values[i % len]) || DEFAULT_COLOR;
    };
  }

  someStyleChanged(change?: IHasChanged) {
    const changed = change?.changed;

    let style = {} as any;

    if (!changed) {
      return;
    }

    for (const opt of Object.keys(changed)) {
      const value = changed[opt];
      if (WATCHED_STYLES.indexOf(opt) === -1) {
        continue;
      }
      switch (opt) {
        // the upstream looks like:
        //    rowBackgroundColor?: (index: number) => string;
        case 'rowBackgroundColor':
        case 'columnBackgroundColor':
          if (value) {
            style[opt] = this.styleFunctor(value);
          } else {
            style[opt] = null;
          }
          break;
        default:
          style[opt] = value;
          break;
      }
    }

    this.style = { ...this.style, ...style };
  }

  protected onSetView() {
    const m = this.view.model;
    m.on('change:cell_renderers', this.onModelCellRenderers, this);
    m.on('change:grid_style', this.onGridStyle, this);
    m.on('change:header_visibility', this.onHeaderVisibility, this);
    m.on(SIZES.map((t) => `change:${t}`).join(' '), this.onModelSize, this);

    this.onModelCellRenderers();
    this.onModelSize();
    setTimeout(() => {
      this.onGridStyle()
        .then(() => {
          this.someStyleChanged({
            changed: this.view.model.get('grid_style').attributes,
          });
        })
        .catch(console.warn);
    }, 100);
  }

  async onGridStyle() {
    let previous = (this.view.model.previousAttributes() as any).style;

    if (previous != null) {
      try {
        previous.off(WATCHED_STYLES, this.someStyleChanged, this);
      } catch (err) {
        console.warn(err);
      }
    }

    let style = this.view.model.get('grid_style') as GridStyleModel;

    if (typeof style === 'string') {
      const promise = this.view.model.widget_manager.get_model(style as any);
      try {
        style = (await promise) as any;
      } catch (err) {
        console.warn(err);
      }
    }

    if (style != null) {
      const init = {} as Record<string, unknown>;
      for (const opt of WATCHED_STYLES) {
        const val = style.get(opt);
        if (val == null) {
          const editor_val = (this.style as any)[opt];
          if (editor_val != null) {
            init[opt] = editor_val;
          }
        }
      }
      if (Object.keys(init)) {
        style.set(init);
        style.save_changes();
      }
      style.on(STYLE_EVENTS, this.someStyleChanged, this);
    }
  }

  setRenderer(rm: CellRendererModel) {
    const region: string = rm.get('region') || 'body';
    const renderers = { [region]: rm.toRenderer(() => this.setRenderer(rm)) };
    this.cellRenderers.update(renderers);
  }

  makeRenderers() {
    let rms: CellRendererModel[] = this._view.model.get('cell_renderers');
    return rms.map((rm) => {
      return {
        region: rm.get('region') || 'body',
        metadata: rm.get('metadata') || {},
        renderer: rm.toRenderer(() => this.setRenderer(rm)),
        model: rm,
      };
    });
  }

  onModelCellRenderers() {
    let renderers = this.makeRenderers();
    (this.cellRenderers as any)._values = {};
    renderers.map((r) => {
      if (r.model) {
        r.model.on('change', () => this.setRenderer(r.model));
      }
      this.cellRenderers.update({ [r.region]: r.renderer });
    });
    if (!renderers.length) {
      this.cellRenderers.update();
    }
  }

  onModelSize() {
    const m = this._view.model;
    const changed = Object.keys(m.changedAttributes());
    const defaultSizes = { ...this.defaultSizes };

    for (const size of changed) {
      let v = m.get(size);
      if (v == null) {
        continue;
      }
      switch (size) {
        default:
          continue;
        case 'row_size':
          defaultSizes.rowHeight = v;
          continue;
        case 'row_header_size':
          defaultSizes.rowHeaderWidth = v;
          continue;
        case 'column_size':
          defaultSizes.columnWidth = v;
          continue;
        case 'column_header_size':
          defaultSizes.columnHeaderHeight = v;
          continue;
      }
    }

    this.defaultSizes = defaultSizes;
  }

  onHeaderVisibility() {
    this.headerVisibility = this.view.model.get('header_visibility');
  }
}
