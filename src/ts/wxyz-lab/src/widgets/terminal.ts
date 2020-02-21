import { Terminal as Xterm } from 'xterm';

import { DOMWidgetView, DOMWidgetModel } from '@jupyter-widgets/base';

import $ from 'jquery';

import { NAME, VERSION } from '..';

import { TerminalPhosphorWidget } from './_terminal';

import { fit } from 'xterm/lib/addons/fit/fit';

const TERMINAL_CLASS = 'jp-WXYZ-Terminal';
// const JP_TERMINAL_CLASS = 'jp-Terminal';
// const JP_TERMINAL_BODY_CLASS = 'jp-Terminal-body';

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
      theme: {
        foreground: '#fff',
        background: '#000',
        cursor: '#fff',
        cursorAccent: '#000',
        selection: 'rgba(255, 255, 255, 0.3)'
      }
    };
  }
}

export class TerminalView extends DOMWidgetView {
  static view_name = 'TerminalView';

  private _term: Xterm;
  private _wrapper: HTMLDivElement;

  _setElement(el: HTMLElement) {
    if (this.pWidget) {
      this.pWidget.dispose();
    }
    this.$el = el instanceof $ ? el : $(el);
    this.el = this.$el[0];
    this.pWidget = new TerminalPhosphorWidget({
      node: el,
      view: this
    });
  }

  render() {
    super.render();
    this.pWidget.addClass(TERMINAL_CLASS);
    this._wrapper = document.createElement('div');
    this.pWidget.node.appendChild(this._wrapper);

    this._term = new Xterm({
      rows: this.model.get('rows'),
      cols: this.model.get('cols'),
      theme: this.model.get('theme')
    });

    setTimeout(() => {
      this._term.open(this._wrapper);

      this.model.on('change:rows change:cols', () => {
        this._term.resize(this.model.get('cols'), this.model.get('rows'));
        // TODO; make this optional
        // fit(this._term);
      });

      this.model.on('msg:custom', this.onCustomMessage, this);
      this.model.on('change:theme', this.onTheme, this);
      this.model.on('change:scroll', this.onScroll, this);

      this._term.onScroll(this.onTermScroll.bind(this));

      this._term.onSelectionChange(this.onTermSelect.bind(this));

      this._term.onData(this.onTermData.bind(this));

      this._term.attachCustomKeyEventHandler(event => {
        if (event.ctrlKey && event.key === 'c' && this._term.hasSelection()) {
          return false;
        }

        return true;
      });

      (this.pWidget as TerminalPhosphorWidget).resized.connect(
        this.onResize,
        this
      );
      this.onResize();
    }, 100);
  }

  // DOM stuff
  onResize() {
    if (this.model.get('fit')) {
      fit(this._term);
    }
  }

  // model events
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
}
