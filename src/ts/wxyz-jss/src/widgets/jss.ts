import {
  DOMWidgetView,
  DOMWidgetModel,
  unpack_models as deserialize
} from '@jupyter-widgets/base';
import { lazyLoader } from '@deathbeds/wxyz-core/lib/widgets/lazy';
import { NAME, VERSION } from '..';

const JSS_CLASS = 'jp-WXYZ-JSSBox';

const _jss = lazyLoader(
  async () => await import(/* webpackChunkName: "jss" */ './_jss')
);

export interface IWidgetModelMap {
  [key: string]: DOMWidgetModel[];
}

export interface IWidgetViewMap {
  [key: string]: DOMWidgetView[];
}

export class JSSModel extends DOMWidgetModel {
  static model_name = 'JSSModel';
  static model_module = NAME;
  static model_module_version = VERSION;
  static view_name = 'JSSView';
  static view_module = NAME;
  static view_module_version = VERSION;

  static serializers = {
    ...DOMWidgetModel.serializers,
    widgets: { deserialize }
  };

  defaults() {
    return {
      ...super.defaults(),
      _model_name: JSSModel.model_name,
      _model_module: NAME,
      _model_module_version: VERSION,
      _view_name: JSSModel.view_name,
      _view_module: NAME,
      _view_module_version: VERSION,
      jss: {},
      widgets: {}
    };
  }

  get widgets() {
    return this.get('widgets') as IWidgetModelMap;
  }
}

export class JSSView extends DOMWidgetView {
  private _style: HTMLStyleElement;
  private _sheet: any; // StyleSheet
  private _addedClasses = new Map<string, DOMWidgetView[]>();

  initialize(options: any) {
    super.initialize(options);
    this.pWidget.addClass(JSS_CLASS);
  }

  get m() {
    return this.model as JSSModel;
  }

  render() {
    super.render();
    this._style = document.createElement('style');
    this.el.appendChild(this._style);
    _jss.load().then(async () => {
      this.m.on('change:jss', this.updateJSS, this);
      this.m.on('change:widgets', this.updateClasses, this);
      await this.updateJSS();
    });
  }

  async updateJSS() {
    let { jss } = await _jss.get();
    let sheet = jss.createStyleSheet(this.m.get('jss'), {
      element: this._style
    });
    this._sheet = sheet;
    this._sheet.attach();
    await this.updateClasses();
  }

  async updateClasses() {
    const { widgets } = this.m;

    this._addedClasses.forEach((views, key) => {
      views.forEach(v => v.pWidget.removeClass(key));
    });

    this._addedClasses.clear();

    for (const jssKey in widgets) {
      const jssClass = this._sheet.classes[jssKey];
      let added = [] as DOMWidgetView[];
      for (const widget of widgets[jssKey]) {
        for (const viewKey in widget.views) {
          const view = await widget.views[viewKey];
          const el = (view as DOMWidgetView).pWidget;
          el.addClass(jssClass);
          added.push(view as DOMWidgetView);
        }
      }
      this._addedClasses.set(jssClass, added);
    }
  }
}
