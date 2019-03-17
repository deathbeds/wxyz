import { DockPanel, DockLayout, Widget } from '@phosphor/widgets';
import {
  JupyterPhosphorWidget,
  DOMWidgetView,
  DOMWidgetModel
} from '@jupyter-widgets/base';

import { Message } from '@phosphor/messaging';
import { toArray } from '@phosphor/algorithm';

export class JupyterPhosphorDockPanelWidget extends DockPanel {
  private _ignoreLayoutChanges: boolean;

  constructor(options: JupyterPhosphorWidget.IOptions & DockPanel.IOptions) {
    let view = options.view;
    delete options.view;
    super(options);
    this._view = view;
    this.layoutModified.connect(this.onLayoutChanged, this);
    view.model.on('change:dock_layout', this.onLayoutModelChanged, this);
  }

  async onLayoutModelChanged() {
    let main = this.jWidgetsToArea(this._view.model.get('dock_layout'));
    this._ignoreLayoutChanges = true;
    if (main) {
      this.restoreLayout({ main });
    }
    setTimeout(() => {
      this._ignoreLayoutChanges = false;
    }, 100);
  }

  onLayoutChanged() {
    if (!this._ignoreLayoutChanges) {
      let layout = this.saveLayout();
      this._view.model.set('dock_layout', this.areaToJWidgets(layout.main));
      this._view.touch();
    }
  }

  areaToJWidgets(area: DockLayout.AreaConfig): object {
    switch (area.type) {
      case 'split-area':
        return {
          ...area,
          children: area.children.map(this.areaToJWidgets, this)
        };
      case 'tab-area':
        return {
          ...area,
          widgets: area.widgets.map(this.findJWidgetModel, this)
        };
      default:
        break;
    }
  }

  findJWidgetModel(pwidget: Widget): number {
    const children: DOMWidgetModel[] = this._view.model.get('children');
    try {
      const model = (pwidget as any)._view.model as DOMWidgetModel;
      return children.indexOf(model);
    } catch (err) {
      return -1;
    }
  }

  findPWidget(childIndex: number): Widget {
    const children: DOMWidgetModel[] = this._view.model.get('children');
    const model = children[childIndex];

    for (let w of toArray(this.widgets())) {
      try {
        let cid = (w as any)._view.model.cid;
        if (cid === model.cid) {
          return w;
        }
      } catch (err) {
        continue;
      }
    }

    return null;
  }

  jWidgetsToArea(json: any): DockLayout.AreaConfig {
    let area = json as DockLayout.AreaConfig;
    switch (area.type) {
      case 'split-area':
        return {
          ...area,
          children: area.children.map(this.jWidgetsToArea, this)
        };
      case 'tab-area':
        return {
          ...area,
          widgets: json.widgets.map(this.findPWidget, this)
        };
      default:
        break;
    }
    return null;
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
    this._ignoreLayoutChanges = true;
    this.addWidget(widget, { mode: 'split-right' });

    const view: DOMWidgetView = (widget as any)._view;
    if (!view) {
      return;
    }
    function onTitle() {
      const {
        description,
        icon_class,
        closable,
        _view_name,
        _model_name
      } = view.model.attributes;
      widget.title.label = description || _view_name || _model_name;
      widget.title.iconClass = `jp-Icon-16 ${icon_class || 'jp-CircleIcon'}`;
      widget.title.closable = closable != null ? closable : true;
    }
    view.model.on(
      'change:description change:icon_class change:closable',
      onTitle
    );
    onTitle();
    setTimeout(() => {
      this._ignoreLayoutChanges = false;
    }, 100);
  }

  private _view: DOMWidgetView;
}
