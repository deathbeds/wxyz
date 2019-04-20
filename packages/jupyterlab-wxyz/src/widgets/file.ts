import { toArray } from '@phosphor/algorithm';
import * as widgets from '@jupyter-widgets/base';
import * as controls from '@jupyter-widgets/controls';

import { NAME, VERSION } from '..';
import { WXYZ, WXYZBox, createWXYZ } from './_base';

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
      }
    }
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
      value: null
    };
  }

  async setFile(file: File) {
    const { name, type, size, lastModified } = file;
    const reader = new FileReader();

    const value = await new Promise<ArrayBuffer>((resolve, reject) => {
      reader.onload = () => resolve(reader.result as ArrayBuffer);
      reader.onerror = () => [reader.abort(), reject()];
      reader.readAsArrayBuffer(file);
    });

    this.set({
      last_modified: lastModified,
      mime_type: type,
      name,
      size,
      value
    });
  }
}

export class FileView extends widgets.DOMWidgetView {
  anchor: HTMLAnchorElement;

  initialize(parameters: any) {
    super.initialize(parameters);
    const m = this.model;
    m.on('change: name', this.onNameChange, this);
    m.on('change: value', this.onValueChange, this);
  }

  render() {
    this.pWidget.addClass('jp-RenderedHTMLCommon');
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
    let url: string = null;
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
      _view_name: FileBoxModel.view_name
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

  initialize(options: any) {
    super.initialize(options);
    const i = (this._input = this.makeInput());
    this.el.appendChild(i);
    this.model.on(
      'change:multiple change:accept',
      this.onInputAttributes,
      this
    );
    this.onInputAttributes();
  }

  protected makeInput() {
    const inp: HTMLInputElement = document.createElement('input');
    inp.type = 'file';
    inp.addEventListener('change', () => this.onInputChange());
    return inp;
  }

  async onInputChange() {
    const children = await Promise.all(
      toArray(this._input.files).map(async file => {
        const child: FileModel = await createWXYZ(
          this.model.widget_manager,
          FileModel.model_name,
          FileModel.view_name,
          {}
        );
        await child.setFile(file);
        child.save_changes();
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
