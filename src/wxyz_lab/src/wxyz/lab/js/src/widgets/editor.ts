import CodeMirror from 'codemirror';

import { Platform } from '@lumino/domutils';
import {
  DOMWidgetView,
  unpack_models as deserialize,
} from '@jupyter-widgets/base';
import { TextareaModel } from '@jupyter-widgets/controls';

import { WXYZ } from '@deathbeds/wxyz-core/lib/widgets/_base';
import { NAME, VERSION } from '..';

import { Mode } from '@jupyterlab/codemirror';

interface IHasChanged {
  changed: { [key: string]: any };
}

const EDITOR_CLASS = 'jp-WXYZ-Editor';

const WATCHED_OPTIONS = [
  // the part between these comments will be rewritten
  // BEGIN SCHEMAGEN:PROPERTIES IEditorConfiguration @61e400d051e0be2c3d80ab6bbc304e616b0dce7729d13c64396b21352cf10855
  'autofocus', 'cursorBlinkRate', 'cursorHeight', 'dragDrop', 'electricChars', 'firstLineNumber', 'fixedGutter', 'flattenSpans', 'foldGutter', 'gutters', 'historyEventDelay', 'indentUnit', 'indentWithTabs', 'keyMap', 'lineNumbers', 'lineWrapping', 'maxHighlightLength', 'mode', 'placeholder', 'pollInterval', 'readOnly', 'rtlMoveVisually', 'scrollbarStyle', 'showCursorWhenSelecting', 'smartIndent', 'tabSize', 'tabindex', 'theme', 'undoDepth', 'viewportMargin', 'workDelay', 'workTime'
  // END SCHEMAGEN:PROPERTIES











];
const WATCHED_EVENTS = WATCHED_OPTIONS.reduce((m, o) => `${m} change:${o}`, '');

/**
 *
 */

export class EditorModeInfoModel extends WXYZ {
  static model_module = NAME;
  static model_module_version = VERSION;
  static model_name = 'EditorModeInfoModel';

  defaults() {
    return {
      ...super.defaults(),
      _model_name: EditorModeInfoModel.model_name,
      _model_module: NAME,
      _model_module_version: VERSION,
      modes: [] as Record<string, unknown>[],
    };
  }

  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
    this.set('modes', Mode.getModeInfo());
    this.save_changes();
  }
}

/** A CodeMirror options for "simple" options (e.g. JSON-compatible)
 */
export class EditorConfigModel extends WXYZ {
  static model_module = NAME;
  static model_module_version = VERSION;
  static model_name = 'EditorConfigModel';

  defaults() {
    return {
      ...super.defaults(),
      _model_name: EditorConfigModel.model_name,
      _model_module: NAME,
      _model_module_version: VERSION,
    };
  }

  to_codemirror() {
    const opts = {} as any;
    for (const opt of WATCHED_OPTIONS) {
      opts[opt] = this.get(opt);
    }
    return opts;
  }
}

export class EditorModel extends TextareaModel {
  static model_name = 'EditorModel';
  static model_module = NAME;
  static model_module_version = VERSION;
  static view_name = 'EditorView';
  static view_module = NAME;
  static view_module_version = VERSION;

  static serializers = {
    ...TextareaModel.serializers,
    config: { deserialize },
  };

  /* the cid of the active scroller */
  scroller: string;

  defaults() {
    return {
      ...super.defaults(),
      _model_name: EditorModel.model_name,
      _model_module: NAME,
      _model_module_version: VERSION,
      _view_name: EditorModel.view_name,
      _view_module: NAME,
      _view_module_version: VERSION,
      description: 'An Editor',
      icon_class: 'jp-EditIcon',
    };
  }
}

export class EditorView extends DOMWidgetView {
  protected _editor: CodeMirror.Editor = null as any;
  model: EditorModel;

  render() {
    super.render();
    this.pWidget.addClass(EDITOR_CLASS);
    this._editor = CodeMirror(this.el);
    this._editor.on('change', () => {
      this.model.set('value', this._editor.getValue());
    });

    this._editor.on('scroll', this.on_editor_scroll);

    this.model.on('change:value', this.value_changed, this);
    this.model.on('change:config', this.config_changed, this);
    this.model.on(
      'change:scroll_x change:scroll_y',
      this.on_scroll_change,
      this
    );

    setTimeout(() => {
      this._editor.refresh();
      this.value_changed();
      const config = this.model.get('config') as EditorConfigModel;
      if (config != null) {
        this.some_config_changed({ changed: config.to_codemirror() });
      }
      this.pWidget.node.addEventListener('keyup', this.handle_keys);
    }, 1);

    this.config_changed();
  }

  handle_keys = (event: KeyboardEvent) => {
    if (Platform.accelKey(event)) {
      if (event.key === 'z') {
        if (event.shiftKey) {
          this._editor.getDoc().redo();
        } else {
          this._editor.getDoc().undo();
        }
        event.preventDefault();
        event.stopPropagation();
      }
    }
  };

  // config
  config_changed() {
    let previous = (this.model.previousAttributes() as any)
      .options as EditorConfigModel;

    if (previous != null) {
      previous.off(WATCHED_EVENTS, this.some_config_changed, this);
    }

    const config = this.model.get('config') as EditorConfigModel;

    if (config != null) {
      const init = {} as Record<string, unknown>;
      for (const opt of WATCHED_OPTIONS) {
        const val = config.get(opt);
        if (val == null) {
          const editor_val = this._editor.getOption(opt);
          if (editor_val != null) {
            init[opt] = editor_val;
          }
        }
      }
      if (Object.keys(init)) {
        config.set(init);
        config.save_changes();
      }
      config.on(WATCHED_EVENTS, this.some_config_changed, this);
    }
  }

  some_config_changed(change?: IHasChanged) {
    const changed = change?.changed;

    if (!changed) {
      return;
    }

    for (const opt of Object.keys(changed)) {
      const value = changed[opt];
      if (value == null || WATCHED_OPTIONS.indexOf(opt) === -1) {
        continue;
      }
      switch (opt) {
        case 'theme':
          if (value && value != 'default') {
            import(`codemirror/theme/${value}.css`).catch(console.warn);
          }
          break;
        case 'mode':
          Mode.ensure(value).catch(console.warn);
          break;
        default:
          break;
      }
      this._editor.setOption(opt, value);
    }

    this._editor.refresh();
  }

  // value
  value_changed() {
    if (this._editor.getValue() !== this.model.get('value')) {
      let value = this.model.get('value');
      if (typeof value !== 'string') {
        value = JSON.stringify(value, null, 2);
      }
      this._editor.setValue(value);
      this.on_editor_scroll();
    }
  }

  get center() {
    const s = this._editor.getScrollInfo();
    const pos = this._editor.coordsChar(s, 'local');
    const center = { scroll_x: pos.ch, scroll_y: pos.line };
    return center;
  }

  // scroll
  on_scroll_change() {
    const scroll = this._editor.getScrollInfo();
    const x = this.model.get('scroll_x');
    const y = this.model.get('scroll_y');
    if (Math.round(scroll.left) === x && Math.round(scroll.top) === y) {
      return;
    }
    this._editor.scrollTo(x, y);
  }

  on_editor_scroll = () => {
    const scroll = this._editor.getScrollInfo();
    const x = this.model.get('scroll_x');
    const y = this.model.get('scroll_y');
    if (Math.round(scroll.left) === x && Math.round(scroll.top) === y) {
      return;
    }
    this.model.set({
      scroll_x: Math.round(scroll.left),
      scroll_y: Math.round(scroll.top),
    });
    this.touch();
  };
}
