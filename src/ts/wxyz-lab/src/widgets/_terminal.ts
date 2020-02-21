import { Widget } from '@phosphor/widgets';
import { Signal } from '@phosphor/signaling';
import { JupyterPhosphorWidget } from '@jupyter-widgets/base/lib/widget';

export class TerminalPhosphorWidget extends JupyterPhosphorWidget {
  private _resized = new Signal<TerminalPhosphorWidget, Widget.ResizeMessage>(
    this
  );

  get resized() {
    return this._resized;
  }

  protected onResize(msg: Widget.ResizeMessage): void {
    super.onResize(msg);
    this.resized.emit(msg);
  }
}
