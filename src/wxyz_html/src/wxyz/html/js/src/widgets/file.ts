import { toArray } from '@lumino/algorithm';
import { JSONExt } from '@lumino/coreutils';
import { Debouncer } from '@lumino/polling';

import * as widgets from '@jupyter-widgets/base';
import * as controls from '@jupyter-widgets/controls';

import { WXYZ, WXYZBox, createModel } from '@deathbeds/wxyz-core';

import { NAME, VERSION } from '../constants';

const CSS = {
  FILE_BOX: 'jp-WXYZ-FileBox',
  FILE_BOX_OVER: 'jp-WXYZ-FileBox-dragover',
  FILE_BOX_TARGET: 'jp-WXYZ-FileBox-DragTarget',
};

export class FileModel extends widgets.DOMWidgetModel {
  static model_name = 'FileModel';
  static view_name = 'FileView';
  static model_module = NAME;
  static model_module_version = NAME;
  static view_module = VERSION;
  static view_module_version = VERSION;

  static serializers = {
    ...WXYZ.serializers,
    value: {
      serialize: (value: ArrayBuffer) => {
        return new DataView((value ? value : new ArrayBuffer(0)).slice(0));
      },
    },
  };

  defaults() {
    return {
      ...super.defaults(),
      _model_name: FileModel.model_name,
      _view_name: FileModel.view_name,
      _model_module: NAME,
      _model_module_version: VERSION,
      _view_module: NAME,
      _view_module_version: VERSION,
      name: 'Untitled.txt',
      mime_type: 'text/plain',
      last_modified: +new Date(),
      size: 0,
      value: null,
    };
  }

  set file(file: File) {
    const reader = new FileReader();

    reader.onload = () => {
      this.set({ value: reader.result });
      this.save_changes();
    };
    reader.readAsArrayBuffer(file);
  }
}

export class TextFileModel extends FileModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: TextFileModel.model_name,
      name: 'untitled.txt',
      mime_type: 'text/plain',
      last_modified: +new Date(),
      size: 0,
      value: '',
    };
  }

  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
    const debouncedText = new Debouncer(this._on_text, 1000);
    const debouncedBytes = new Debouncer(this._on_bytes, 1000);
    this.on('change:text', () => debouncedText.invoke(), this);
    this.on('change:value', () => debouncedBytes.invoke(), this);
  }

  _on_text() {
    const text = this.get('text');
    const value = str2ab(text);
    if (value && value !== this.get('value')) {
      setTimeout(() => {
        this.set({ value });
        this.save_changes();
      }, 100);
    }
  }

  _on_bytes() {
    let value = this.get('value') as string | ArrayBuffer | DataView;
    let text: string;
    let buffer: ArrayBuffer;

    if (value instanceof ArrayBuffer) {
      buffer = value;
    } else if (value instanceof DataView) {
      buffer = value.buffer;
    } else {
      text = value;
    }

    if (buffer != null) {
      text = String.fromCharCode.apply(null, new Uint8Array(buffer));
    }

    const old_text = this.get('text');

    if (text && text !== old_text) {
      setTimeout(() => {
        this.set({ text });
        this.save_changes();
      }, 100);
    }
  }
}

export class JSONFileModel extends FileModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: JSONFileModel.model_name,
      name: 'Untitled.json',
      mime_type: 'application/json',
      last_modified: +new Date(),
      size: 2,
      value: '{}',
    };
  }

  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
    const debouncedJson = new Debouncer(this._on_json, 1000);
    const debouncedBytes = new Debouncer(this._on_bytes, 1000);
    this.on('change:json', () => debouncedJson.invoke(), this);
    this.on('change:value', () => debouncedBytes.invoke(), this);
  }

  _on_json() {
    const json = this.get('json');
    const value = str2ab(JSON.stringify(json, null, 2));
    if (value && value !== this.get('value')) {
      setTimeout(() => {
        this.set({ value });
        this.save_changes();
      }, 100);
    }
  }

  _on_bytes() {
    let value = this.get('value') as string | ArrayBuffer | DataView;
    let json_str: string;
    let buffer: ArrayBuffer;

    if (value instanceof ArrayBuffer) {
      buffer = value;
    } else if (value instanceof DataView) {
      buffer = value.buffer;
    } else {
      json_str = value;
    }

    if (buffer != null) {
      json_str = String.fromCharCode.apply(null, new Uint8Array(buffer));
    }

    const json = JSON.parse(json_str);

    const old_json = this.get('json');

    if (json && !JSONExt.deepEqual(json, old_json)) {
      setTimeout(() => {
        this.set({ json });
        this.save_changes();
      }, 100);
    }
  }
}

export class FileView extends widgets.DOMWidgetView {
  anchor: HTMLAnchorElement;

  initialize(parameters: any) {
    super.initialize(parameters);
    const m = this.model;
    m.on('change:name', this.onNameChange, this);
    m.on('change:value', this.onValueChange, this);
  }

  render() {
    this.luminoWidget.addClass('jp-RenderedHTMLCommon');
    this.anchor = document.createElement('a');
    this.anchor.target = '_blank';
    this.el.appendChild(this.anchor);
    this.onNameChange();
    this.onValueChange();
  }

  onNameChange() {
    const name = this.model.get('name');
    this.anchor.text = this.anchor.download = name;
  }

  onValueChange() {
    if (this.anchor.href) {
      URL.revokeObjectURL(this.anchor.href);
    }
    const value: ArrayBuffer = this.model.get('value');
    let url: string = '#';
    if (value != null) {
      let blob = new Blob([value], { type: this.model.get('mime_type') });
      url = URL.createObjectURL(blob);
    }
    this.anchor.href = url;
  }
}

export class FileBoxModel extends WXYZBox {
  static model_name = 'FileBoxModel';
  static view_name = 'FileBoxView';

  defaults() {
    return {
      ...super.defaults(),
      _model_name: FileBoxModel.model_name,
      _view_name: FileBoxModel.view_name,
    };
  }

  get multiple(): boolean {
    let multiple = this.get('multiple');
    return multiple == null ? true : multiple;
  }

  get accept(): string {
    let accept = this.get('accept');
    return accept == null ? '' : accept.join(',');
  }
}

export class FileBoxView extends controls.BoxView {
  private _input: HTMLInputElement;
  model: FileBoxModel;

  events() {
    return {
      dragenter: 'onDragEnter',
      dragover: 'onDragOver',
      dragleave: 'onDragLeave',
      dragend: 'onDragLeave',
      dragexit: 'onDragLeave',
      drop: 'onDrop',
    };
  }

  initialize(options: any) {
    super.initialize(options);
    const i = (this._input = this.makeInput());
    const t = this.makeTarget();
    this.el.appendChild(i);
    this.el.appendChild(t);
    this.model.on('change:multiple change:accept', this.onInputAttributes, this);
    this.onInputAttributes();
  }

  onDragEnter(evt: DragEvent) {
    evt.stopPropagation();
    evt.preventDefault();
  }

  onDragOver(evt: DragEvent) {
    evt.stopPropagation();
    evt.preventDefault();
    this.luminoWidget.addClass(CSS.FILE_BOX_OVER);
  }

  onDragLeave(_: DragEvent) {
    this.luminoWidget.removeClass(CSS.FILE_BOX_OVER);
  }

  onDrop(evt: DragEvent) {
    evt.stopPropagation();
    evt.preventDefault();
    this.luminoWidget.removeClass(CSS.FILE_BOX_OVER);
    this._input.files = evt.dataTransfer.files;
    this.onInputChange().catch(console.warn);
  }

  protected makeInput() {
    const inp: HTMLInputElement = document.createElement('input');
    inp.type = 'file';
    inp.addEventListener('change', () => this.onInputChange());
    return inp;
  }

  protected makeTarget() {
    const tgt = document.createElement('div');
    tgt.className = CSS.FILE_BOX_TARGET;
    return tgt;
  }

  async onInputChange() {
    const children = await Promise.all(
      toArray(this._input.files).map(async (file) => {
        const { name, type, size, lastModified } = file;
        const child: FileModel = await createModel(
          this.model.widget_manager,
          NAME,
          FileModel.model_name,
          FileModel.view_name,
          {
            last_modified: lastModified,
            mime_type: type,
            name,
            size,
          }
        );
        child.file = file;
        return child;
      })
    );
    this.model.set({ children });
    this.touch();
  }

  onInputAttributes() {
    const i = this._input;
    const m = this.model;
    i.multiple = m.multiple;
    i.accept = m.accept;
  }
}

// function ab2str(buf: ArrayBuffer) {
//   return String.fromCharCode.apply(null, new Uint16Array(buf));
// }

function str2ab(str: string) {
  let buf = new ArrayBuffer(str.length); // 2 bytes for each char
  let bufView = new Uint8Array(buf);
  for (let i = 0, strLen = str.length; i < strLen; i++) {
    bufView[i] = str.charCodeAt(i);
  }
  return buf;
}
