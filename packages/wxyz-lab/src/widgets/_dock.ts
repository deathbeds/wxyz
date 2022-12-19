import { toArray } from '@lumino/algorithm';
import { Application } from '@lumino/application';
import { Message } from '@lumino/messaging';
import { DockLayout, DockPanel, Widget } from '@lumino/widgets';

import { DockPanelSvg } from '@jupyterlab/ui-components';

import {
  DOMWidgetModel,
  DOMWidgetView,
  JupyterLuminoWidget,
} from '@jupyter-widgets/base';

export const CSS = {
  HIDE_TABS: 'jp-WXYZ-DockBox-hide-tabs',
  DOCK_BOX: 'jp-WXYZ-DockBox',
};

let nextId = 0;

export class JupyterPhosphorDockPanelWidget extends DockPanelSvg {
  protected _view: DOMWidgetView;
  private _style: HTMLStyleElement;
  private _defaultSpacing: number;

  constructor(options: JupyterLuminoWidget.IOptions & DockPanel.IOptions) {
    let view = options.view;
    delete options.view;
    super(options);
    this.addClass(CSS.DOCK_BOX);
    this.id = this.id || `${CSS.DOCK_BOX}-${nextId++}`;
    this._view = view;
    this.layoutModified.connect(this.onLayoutChanged, this);
    view.model.on('change:dock_layout', () => this.onLayoutModelChanged());
    view.model.on(
      'change:hide_tabs change:tab_size change:border_size',
      this.onStyleChanged,
      this
    );
    view.model.on('change:spacing', this.onSpacing, this);
    this._style = document.createElement('style');
    this.onStyleChanged();
    this._defaultSpacing = this.spacing;
    this.onSpacing();
    document.head.appendChild(this._style);
  }

  onSpacing() {
    let spacing = this._view.model.get('spacing');
    this.spacing = spacing == null ? this._defaultSpacing : spacing;
  }

  onStyleChanged() {
    let styles: string[] = [];
    let size = (this._view.model.get('tab_size') || '').trim();
    let border = (this._view.model.get('border_size') || '').trim();
    let hideTabs = this._view.model.get('hide_tabs') || false;

    if (hideTabs) {
      styles.push(`
        #${this.id} .lm-DockPanel-tabBar[data-orientation='horizontal'] {
          min-height: 0;
          max-height: 0;
          border: 0;
          margin: 0;
          padding: 0;
          visibility: hidden;
          height: 0 !important;
        }
        `);
    } else if (size.length) {
      styles.push(`
        #${this.id} {
          --jp-private-horizontal-tab-height: ${size};
        }
      `);
    }

    if (border.length) {
      styles.push(`
        #${this.id} {
          --jp-border-width: ${border};
        }
      `);
    }

    this._style.textContent = styles.join('\n');
    this.onSpacing();
  }

  async onLayoutModelChanged(dockLayout?: any) {
    dockLayout = dockLayout != null ? dockLayout : this._view.model.get('dock_layout');
    let main = this.jWidgetsToArea(dockLayout);
    if (main) {
      this.restoreLayout({ main });
      this.onSpacing();
    }
  }

  onLayoutChanged() {
    let { main } = this.saveLayout();
    if (!main) {
      return;
    }
    this._view.model.set('dock_layout', this.areaToJWidgets(main));
    this._view.touch();
  }

  /* TODO: a better typing */
  areaToJWidgets(area: DockLayout.AreaConfig): any {
    switch (area.type) {
      case 'split-area':
        return {
          ...area,
          // normalize the sizes to avoid thrashing
          sizes: area.sizes.map((size) => Math.floor(10000 * size) / 10000),
          children: area.children.map(this.areaToJWidgets, this),
        };
      case 'tab-area':
        return {
          ...area,
          widgets: area.widgets.map(this.findJWidgetModel, this),
        };
      default:
        break;
    }
  }

  findJWidgetModel(pwidget: Widget): number {
    const children: DOMWidgetModel[] = this._view.model.get('children');
    const model = (pwidget as any)._view.model as DOMWidgetModel;
    return children.indexOf(model);
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
          children: area.children.map(this.jWidgetsToArea, this),
        };
      case 'tab-area':
        return {
          ...area,
          widgets: json.widgets.map(this.findPWidget, this),
        };
      default:
        break;
    }
    return null;
  }

  processMessage(msg: Message) {
    super.processMessage(msg);
    this._view.processLuminoMessage(msg);
  }

  dispose() {
    if (this.isDisposed) {
      return;
    }
    super.dispose();
    if (this._view) {
      this._view.remove();
    }
    this._view = null as unknown as DOMWidgetView;
  }

  insertWidget(i: number, widget: Widget) {
    this.addWidget(widget, { mode: 'split-right' });

    const view: DOMWidgetView = (widget as any)._view;
    if (!view) {
      return;
    }
    function onTitle() {
      const { description, icon_class, closable, _view_name, _model_name } =
        view.model.attributes;
      widget.title.label = description || _view_name || _model_name;
      widget.title.iconClass = `jp-Icon-16 ${icon_class || 'jp-CircleIcon'}`;
      widget.title.closable = closable != null ? closable : true;
    }
    view.model.on('change:description change:icon_class change:closable', onTitle);
    onTitle();
  }
}

export class JupyterLabPhosphorDockPanelWidget extends JupyterPhosphorDockPanelWidget {
  app: Application<Widget>;

  insertWidget(i: number, widget: Widget) {
    super.insertWidget(i, widget);
    const mode = this._view.model.get('mode') || 'tab-after';
    widget.id = widget.id || `jp-WXYZ-DockPop-pop-${nextId++}`;
    (this.app.shell as any).add(widget, 'main', { mode });
  }
}
