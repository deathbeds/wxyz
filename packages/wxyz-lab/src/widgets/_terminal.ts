import { Message } from '@lumino/messaging';
import { Signal } from '@lumino/signaling';
import { Widget } from '@lumino/widgets';

import { JupyterLuminoWidget } from '@jupyter-widgets/base';

export class TerminalLuminoWidget extends JupyterLuminoWidget {
  private _resized = new Signal<TerminalLuminoWidget, Widget.ResizeMessage>(this);

  private _shown = new Signal<TerminalLuminoWidget, Message>(this);
  get resized() {
    return this._resized;
  }

  get shown() {
    return this._shown;
  }

  dispose() {
    super.dispose();
  }

  protected onResize(msg: Widget.ResizeMessage): void {
    super.onResize(msg);
    this.resized.emit(msg);
  }

  protected onUpdateRequest(msg: Message) {
    super.onUpdateRequest(msg);
    if (this.isVisible) {
      this.shown.emit(msg);
    }
  }
}
