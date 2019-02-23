import { DockPanel, Widget } from '@phosphor/widgets';
import { JupyterPhosphorWidget, DOMWidgetView } from '@jupyter-widgets/base';

import { Message } from '@phosphor/messaging';

export class JupyterPhosphorDockPanelWidget extends DockPanel {
  constructor(options: JupyterPhosphorWidget.IOptions & DockPanel.IOptions) {
    let view = options.view;
    delete options.view;
    super(options);
    this._view = view;
  }

  processMessage(msg: Message) {
    super.processMessage(msg);
    this._view.processPhosphorMessage(msg);
  }

  dispose() {
    if (this.isDisposed) {
      return;
    }
    super.dispose();
    if (this._view) {
      this._view.remove();
    }
    this._view = (null as unknown) as DOMWidgetView;
  }

  insertWidget(i: number, widget: Widget) {
    this.addWidget(widget, { mode: 'split-right' });

    const view: DOMWidgetView = (widget as any)._view;
    if (!view) {
      return;
    }
    function onTitle() {
      const { description, icon_class, closable } = view.model.attributes;
      widget.title.label = description || `A Widget`;
      widget.title.iconClass = `jp-Icon-16 ${icon_class || 'jp-CircleIcon'}`;
      widget.title.closable = closable != null ? closable : true;
    }
    view.model.on(
      'change:description change:icon_class change:closable',
      onTitle
    );
    onTitle();
  }

  private _view: DOMWidgetView;
}
