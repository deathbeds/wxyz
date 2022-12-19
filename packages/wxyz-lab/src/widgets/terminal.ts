import { ITerminalOptions, Terminal as Xterm } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';

import { DOMWidgetModel, DOMWidgetView } from '@jupyter-widgets/base';

import { NAME, VERSION } from '../constants';

import { TerminalLuminoWidget } from './_terminal';

const TRAITS = {
  allow_transparency: 'allowTransparency',
  bell_sound: 'bellSound',
  bell_style: 'bellStyle',
  cancel_events: 'cancelEvents',
  colors: 'colors',
  convert_eol: 'convertEol',
  cursor_blink: 'cursorBlink',
  cursor_style: 'cursorStyle',
  debug: 'debug',
  disable_stdin: 'disableStdin',
  enable_bold: 'enableBold',
  font_family: 'fontFamily',
  font_size: 'fontSize',
  font_weight: 'fontWeight',
  font_weight_bold: 'fontWeightBold',
  letter_spacing: 'letterSpacing',
  line_height: 'lineHeight',
  mac_option_is_meta: 'macOptionIsMeta',
  pop_on_bell: 'popOnBell',
  renderer_type: 'rendererType',
  right_click_selects_word: 'rightClickSelectsWord',
  screen_keys: 'screenKeys',
  scrollback: 'scrollback',
  tab_stop_width: 'tabStopWidth',
  term_name: 'termName',
  use_flow_control: 'useFlowControl',
  visual_bell: 'visualBell',
} as { [key: string]: string };

const TERMINAL_CLASS = 'jp-WXYZ-Terminal';
// const JP_TERMINAL_CLASS = 'jp-Terminal';
// const JP_TERMINAL_BODY_CLASS = 'jp-Terminal-body';

function _makeListener(view: TerminalView, traitName: string, attrName: string) {
  view.model.on(`change:${traitName}`, () =>
    view.setTermOption(attrName, view.model.get(traitName))
  );
}

export class TerminalModel extends DOMWidgetModel {
  static model_name = 'TerminalModel';
  static model_module = NAME;
  static model_module_version = VERSION;
  static view_name = 'TerminalView';
  static view_module = NAME;
  static view_module_version = VERSION;

  defaults() {
    return {
      ...super.defaults(),
      _model_name: TerminalModel.model_name,
      _model_module: NAME,
      _model_module_version: VERSION,
      _view_name: TerminalView.view_name,
      _view_module: NAME,
      _view_module_version: VERSION,
      description: 'A Terminal',
      icon_class: 'jp-TerminalIcon',
      rows: 24,
      cols: 80,
      scroll: 0,
      selection: '',
      local_echo: false,
      fit: true,
      active_terminals: 0,
      theme: {
        foreground: '#fff',
        background: '#000',
        cursor: '#fff',
        cursorAccent: '#000',
        selection: 'rgba(255, 255, 255, 0.3)',
      },
    };
  }
}

export class TerminalView extends DOMWidgetView {
  static view_name = 'TerminalView';

  luminoWidget: TerminalLuminoWidget;

  protected _term: Xterm;
  protected _fitAddon: FitAddon;
  private _wasInitialized = false;
  _setElement(el: HTMLElement) {
    const { $ } = window.Backbone;

    if (this.luminoWidget) {
      this.luminoWidget.dispose();
    }
    this.$el = el instanceof $ ? el : $(el);
    this.el = this.$el[0];
    this.luminoWidget = new TerminalLuminoWidget({
      node: el,
      view: this,
    });
  }

  setTermOption(attr: string, value: any) {
    if ((this._term.options as any)[attr] !== value) {
      (this._term.options as any)[attr] = value;
    }
  }

  getOptions(): ITerminalOptions {
    const m = this.model;

    const opts: ITerminalOptions = {
      rows: m.get('rows'),
      cols: m.get('cols'),
      theme: m.get('theme'),
    };

    for (const trait of Object.keys(TRAITS)) {
      const value = m.get(trait);
      if (value != null) {
        (opts as any)[TRAITS[trait]] = value;
      }
    }
    return opts;
  }

  render() {
    super.render();
    this.luminoWidget.addClass(TERMINAL_CLASS);

    this._term = new Xterm(this.getOptions());
    this._fitAddon = new FitAddon();
    this._term.loadAddon(this._fitAddon);

    if (this.luminoWidget.isVisible) {
      this.onInit();
    } else {
      setTimeout(() => this.onInit(), 200);
      this.luminoWidget.shown.connect(this.onResize, this);
    }
  }

  onInit() {
    if (this._wasInitialized) {
      return;
    }
    this._term.open(this.luminoWidget.node);

    this.model.on('change:rows change:cols change:fit', this.onModelResize, this);

    this.model.on('msg:custom', this.onCustomMessage, this);
    this.model.on('change:theme', this.onTheme, this);
    this.model.on('change:scroll', this.onScroll, this);

    for (const traitName of Object.keys(TRAITS)) {
      _makeListener(this, traitName, TRAITS[traitName]);
    }

    this._term.onScroll(this.onTermScroll.bind(this));

    this._term.onSelectionChange(this.onTermSelect.bind(this));

    this._term.onData(this.onTermData.bind(this));
    this._term.onResize(this.onTermResize.bind(this));

    this._term.attachCustomKeyEventHandler((event) => {
      if (event.ctrlKey && event.key === 'c' && this._term.hasSelection()) {
        return false;
      }

      return true;
    });

    this.luminoWidget.resized.connect(this.onResize, this);
    this.luminoWidget.disposed.connect(this.onDispose, this);
    this.onResize();
    this.model.set('active_terminals', (this.model.get('active_terminals') || 0) + 1);
    this._wasInitialized = true;
    this.touch();
  }

  onDispose() {
    this._term.dispose();
    this.luminoWidget.resized.disconnect(this.onResize, this);
    this.luminoWidget.disposed.disconnect(this.onDispose, this);
    this.model.set('active_terminals', this.model.get('active_terminals') - 1);
  }

  // DOM stuff
  onResize() {
    if (this.model.get('fit')) {
      this._fitAddon.fit();
    }
  }

  // model events
  onModelResize() {
    if (this.model.get('fit')) {
      this.onResize();
      return;
    }
    const rows = this.model.get('rows');
    const cols = this.model.get('cols');

    if (this._term.rows !== rows || this._term.cols !== cols) {
      this._term.resize(rows, cols);
    }
  }

  onCustomMessage(msg: any) {
    this._term.write(msg.content as string);
  }

  onTheme() {
    this._term.setOption('theme', this.model.get('theme'));
  }

  onScroll() {
    this._term.scrollToLine(this.model.get('scroll'));
  }

  // terminal events
  onTermSelect() {
    const selection = this._term.getSelection();
    this.model.set({ selection });
    this.touch();
  }

  onTermScroll(scroll: number) {
    this.model.set({ scroll });
    this.touch();
  }

  onTermData(data: string) {
    this.model.send({ content: data }, {});
    if (this.model.get('local_echo')) {
      this._term.write(data);
    }
  }

  onTermResize({ cols, rows }: { cols: number; rows: number }) {
    const m = this.model;
    if (m.get('cols') === cols && m.get('rows') === rows) {
      return;
    }
    m.set({ cols, rows });
    this.touch();
  }
}
