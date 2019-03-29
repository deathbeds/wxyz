import { Message } from '@phosphor/messaging';

import { StyleGrid } from './stylegrid';

export class SelectGrid extends StyleGrid {
  protected _scrollLock = false;

  protected onBeforeAttach(msg: Message): void {
    ['touchstart', 'touchend', 'touchmove', 'mouseup'].forEach(evt =>
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
    this._view.touch();
  }

  handleEvent(evt: Event) {
    super.handleEvent(evt);
    switch (evt.type) {
      default:
        break;
      case 'touchstart':
      case 'mousedown':
        console.log(evt.type, evt);
        break;
      case 'touchend':
      case 'mouseup':
        console.log(evt.type, evt);
        break;
      case 'touchmove':
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

    this.view.touch();
  }

  onSetView() {
    this.view.model.on(
      'change:scroll_x change:scroll_y',
      this.onModelScroll,
      this
    );
    this.onModelScroll();
  }

  onModelScroll() {
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
