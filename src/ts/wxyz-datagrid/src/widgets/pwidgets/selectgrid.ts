import { Message } from '@lumino/messaging';
import { Widget } from '@lumino/widgets';

import { StyleGrid } from './stylegrid';

import { SectionList } from '@lumino/datagrid/lib/sectionlist';

export class SelectGrid extends StyleGrid {
  protected _scrollLock = false;

  protected onBeforeAttach(msg: Message): void {
    ['touchmove', 'mouseup'].forEach(evt =>
      this.node.addEventListener(evt, this)
    );
    super.onBeforeAttach(msg);
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
      case 'touchmove':
      case 'mousemove':
        this.updateHover(evt as MouseEvent);
        break;
      case 'wheel':
        this.updateViewport();
        break;
    }
    if (this._view.model.changedAttributes()) {
      this._view.touch();
    }
  }

  hoveredCell(evt: Event) {
    const { offsetX, offsetY } = evt as MouseEvent;
    const { headerWidth, headerHeight } = this;
    const r1 = (this as any)._rowSections.indexOf(
      offsetY - headerHeight + this.scrollY
    );
    const c1 = (this as any)._columnSections.indexOf(
      offsetX - headerWidth + this.scrollX
    );
    return [c1, r1];
  }

  viewExtent() {
    const { headerWidth, headerHeight, scrollX, scrollY } = this;
    const rows: SectionList = (this as any)._rowSections;
    const cols: SectionList = (this as any)._columnSections;

    const x = scrollX - headerWidth;
    const y = scrollY - headerHeight;

    const vc = cols.indexOf(x) + 1;
    const vr = rows.indexOf(y) + 1;

    const vc1 = cols.indexOf(x + this.viewportWidth);
    const vr1 = rows.indexOf(y + this.viewportHeight);

    return [vc, vc1, vr, vr1];
  }

  updateViewport(): void {
    const [vc, vc1, vr, vr1] = this.viewExtent();
    const m = this._view.model;
    m.set({ viewport: [vc, vc1, vr, vr1] });
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
    const m = this.view.model;
    const [vc, vc1, vr, vr1] = this.viewExtent();
    let [mvc, mvc1, mvr, mvr1] = m.get('viewport');
    if (vc !== mvc || vc1 !== mvc1 || vr !== mvr || vr1 !== mvr1) {
      this.scrollTo(
        mvc * this.defaultSizes.columnWidth,
        mvr * this.defaultSizes.rowHeight
      );
    }
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
