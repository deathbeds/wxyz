import { Widget } from '@phosphor/widgets';
import { Signal } from '@phosphor/signaling';
import { Message } from '@phosphor/messaging';
import { JupyterPhosphorWidget } from '@jupyter-widgets/base/lib/widget';

export class TerminalPhosphorWidget extends JupyterPhosphorWidget {
  private _resized = new Signal<TerminalPhosphorWidget, Widget.ResizeMessage>(
    this
  );

  private _shown = new Signal<TerminalPhosphorWidget, Message>(this);
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
