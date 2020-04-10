import { Message } from '@lumino/messaging';
import { Widget } from '@lumino/widgets';

import { StyleGrid } from './stylegrid';

import { CellRenderer, TextRenderer } from '@lumino/datagrid';
// import { SectionList } from '@lumino/datagrid/lib/sectionlist';

const SELECT_COLOR = 'rgba(0,0,255,0.125)';

export const selectedFunc: CellRenderer.ConfigFunc<string> = config => {
  let selection: number[] = null;
  let jmodel: any;
  try {
    jmodel = (config.metadata as any).jmodel;
    // this is the `attributes` of the Jupyter Widget model
    selection = jmodel.selection;
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
    let selectionColor = jmodel ? jmodel.selection_color : '';
    return selectionColor || SELECT_COLOR;
  }
  return 'rgba(0,0,0,0)';
};

export class SelectGrid extends StyleGrid {
  protected _scrollLock = false;

  protected onBeforeAttach(msg: Message): void {
    ['touchstart', 'touchend', 'touchmove', 'mouseup'].forEach(evt =>
      this.node.addEventListener(evt, this)
    );
    super.onBeforeAttach(msg);
  }

  makeRenderers() {
    return [
      {
        region: 'body',
        metadata: null,
        renderer: new TextRenderer({ backgroundColor: selectedFunc }),
        model: null
      },
      ...super.makeRenderers()
    ];
  }

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
    this.updateViewport();
    this._view.touch();
  }

  onResize(msg: Widget.ResizeMessage) {
    super.onResize(msg);
    this.updateViewport();
    this._view.touch();
  }

  handleEvent(evt: Event) {
    super.handleEvent(evt);
    switch (evt.type) {
      default:
        break;
      case 'touchstart':
      case 'mousedown':
        this.onSelectStart(evt);
        break;
      case 'touchend':
      case 'mouseup':
        if (this._view.model.get('selecting')) {
          this.onSelectEnd(evt);
        }
        break;
      case 'touchmove':
      case 'mousemove':
        this.updateHover(evt as MouseEvent);
        if (this._view.model.get('selecting')) {
          this.onSelect(evt);
        }
        break;
      case 'wheel':
        this.updateViewport();
        break;
    }
    if (this._view.model.changedAttributes()) {
      this._view.touch();
    }
  }

  onSelectStart(_: Event) {
    let m = this._view.model;
    const s = m.get('selection');
    const [c, r] = this.hoveredCell(_);
    if ((_ as MouseEvent).shiftKey) {
      m.set({
        selection: [s[0], c, s[2], r],
        selecting: false
      });
    } else {
      m.set({
        selection: [c, c, r, r],
        selecting: true
      });
    }
    this._view.touch();
    // this.repaint();
  }

  onSelect(evt: Event) {
    let m = this._view.model;
    let s = m.get('selection') || [0, 0, 0, 0];
    const [c1, r1] = this.hoveredCell(evt);
    let n = [s[0], c1, s[2], r1];
    m.set({ selection: n });
    this._view.touch();
    // this.repaint();
  }

  onSelectEnd(evt: Event) {
    const [c1, r1] = this.hoveredCell(evt);
    const old = this._view.model.get('selection');

    this._view.model.set({
      selecting: false,
      selection: [old[0], c1, old[2], r1]
    });

    this._view.touch();
    // this.repaint();
  }

  hoveredCell(evt: Event) {
    const { offsetX, offsetY } = evt as MouseEvent;
    const { headerWidth, headerHeight } = this;
    const r1 = (this as any)._rowSections.sectionIndex(
      offsetY - headerHeight + this.scrollY
    );
    const c1 = (this as any)._columnSections.sectionIndex(
      offsetX - headerWidth + this.scrollX
    );
    return [c1, r1];
  }

  // viewExtent() {
  //   const { headerWidth, headerHeight, scrollX, scrollY } = this;
  //   const rows: SectionList = (this as any)._rowSections;
  //   const cols: SectionList = (this as any)._columnSections;

  //   const x = scrollX - headerWidth;
  //   const y = scrollY - headerHeight;

  //   const vc = cols.sectionIndex(x) + 1;
  //   const vr = rows.sectionIndex(y) + 1;

  //   const vc1 = cols.sectionIndex(x + this.viewportWidth);
  //   const vr1 = rows.sectionIndex(y + this.viewportHeight);

  //   return [vc, vc1, vr, vr1];
  // }

  updateViewport(): void {
  //   const [vc, vc1, vr, vr1] = this.viewExtent();
  //   const m = this._view.model;
  //   m.set({ viewport: [vc, vc1, vr, vr1] });
  }

  updateHover(evt: MouseEvent): void {
    const m = this._view.model;
    const [c, r] = this.hoveredCell(evt);
    m.set({
      hover_row: r,
      hover_column: c
    });
  }

  protected onSetView() {
    super.onSetView();
    this.view.model.on('change:viewport', this.onModelViewport, this);
    this.view.model.on(
      'change:scroll_x change:scroll_y',
      this.onModelScroll,
      this
    );
    this.onModelScroll();
    this.onModelViewport();
  }

  protected onModelViewport() {
    // const m = this.view.model;
    // const [vc, vc1, vr, vr1] = this.viewExtent();
    // let [mvc, mvc1, mvr, mvr1] = m.get('viewport');
    // if (vc !== mvc || vc1 !== mvc1 || vr !== mvr || vr1 !== mvr1) {
    //   console.log('scroll');
    //   // this.scrollTo(mvc * this.baseColumnSize, mvr * this.rowSize('foo'));
    // }
  }

  protected onModelScroll() {
    const m = this.view.model;
    let x = m.get('scroll_x');
    let y = m.get('scroll_y');
    if (x != null && y != null) {
      this._scrollLock = true;
      this.scrollTo(x, y);
      this._scrollLock = false;
    }
  }
}
