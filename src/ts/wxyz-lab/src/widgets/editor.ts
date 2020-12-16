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
  // BEGIN SCHEMAGEN:PROPERTIES IEditorConfiguration
  'autofocus',
  'cursorBlinkRate',
  'cursorHeight',
  'dragDrop',
  'electricChars',
  'firstLineNumber',
  'fixedGutter',
  'flattenSpans',
  'foldGutter',
  'gutters',
  'historyEventDelay',
  'indentUnit',
  'indentWithTabs',
  'keyMap',
  'lineNumbers',
  'lineWrapping',
  'maxHighlightLength',
  'mode',
  'placeholder',
  'pollInterval',
  'readOnly',
  'rtlMoveVisually',
  'scrollbarStyle',
  'showCursorWhenSelecting',
  'smartIndent',
  'tabSize',
  'tabindex',
  'theme',
  'undoDepth',
  'viewportMargin',
  'workDelay',
  'workTime',
  // END SCHEMAGEN:PROPERTIES
];
const WATCHED_EVENTS = WATCHED_OPTIONS.reduce((m, o) => `${m} change:${o}`, '');

/** A CodeMirror options for "simple" options
 *
 * TODO: generate a JSON schema and kernel widget class
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
  private _editor: CodeMirror.Editor = null as any;

  render() {
    super.render();
    this.pWidget.addClass(EDITOR_CLASS);
    this._editor = CodeMirror(this.el);
    this._editor.on('change', () => {
      this.model.set('value', this._editor.getValue());
      this.touch();
    });

    this.model.on('change:value', this.value_changed, this);
    this.model.on('change:config', this.config_changed, this);

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

  config_changed() {
    let previous = (this.model.previousAttributes() as any)
      .options as EditorConfigModel;

    if (previous != null) {
      previous.off(WATCHED_EVENTS, this.some_config_changed, this);
    }

    const opts = this.model.get('config') as EditorConfigModel;

    if (opts != null) {
      opts.on(WATCHED_EVENTS, this.some_config_changed, this);
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
          if (value) {
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

  value_changed() {
    if (this._editor.getValue() !== this.model.get('value')) {
      let value = this.model.get('value');
      if (typeof value !== 'string') {
        value = JSON.stringify(value, null, 2);
      }
      this._editor.setValue(value);
    }
  }
}
