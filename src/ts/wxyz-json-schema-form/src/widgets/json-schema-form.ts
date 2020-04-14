import { JSONExt } from '@lumino/coreutils';

import { BoxView } from '@jupyter-widgets/controls';

import { RenderedMarkdown } from '@jupyterlab/rendermime';
import * as _schemaform from '@deathbeds/jupyterlab-rjsf/lib/schemaform';
import { IRenderMimeRegistry } from '@jupyterlab/rendermime';

import { lazyLoader } from '@deathbeds/wxyz-core/lib/widgets/lazy';
import { WXYZBox } from '@deathbeds/wxyz-core/lib/widgets/_base';
import { NAME, VERSION } from '..';

const _dbjrjsf = lazyLoader(
  async () => await import('@deathbeds/jupyterlab-rjsf/lib/schemaform')
);

const FORM_CLASS = 'jp-WXYZ-JSONSchemaForm';
const INNER_CLASS = 'jp-WXYZ-JSONSchemaForm-Inner';

export class JSONSchemaFormModel extends WXYZBox {
  static model_name = 'JSONSchemaFormModel';
  static model_module = NAME;
  static model_module_version = VERSION;
  static view_name = 'JSONSchemaFormView';
  static view_module = NAME;
  static view_module_version = VERSION;

  defaults() {
    return {
      ...super.defaults(),
      _model_name: JSONSchemaFormModel.model_name,
      _model_module: NAME,
      _model_module_version: VERSION,
      _view_name: JSONSchemaFormModel.view_name,
      _view_module: NAME,
      _view_module_version: VERSION,
      value: {} as any,
      schema: {} as any,
      ui_schema: {} as any,
      errors: []
    };
  }

  get formData(): any {
    return this.get('value') || null;
  }

  set formData(formData) {
    if (!JSONExt.deepEqual(formData, this.formData)) {
      this.set('value', formData);
    }
  }

  get schema(): any {
    return this.get('schema') || {};
  }

  get uiSchema(): any {
    return this.get('ui_schema') || {};
  }

  get errors(): any[] {
    return this.get('errors') || [];
  }

  set errors(errors) {
    this.set('errors', errors);
  }
}

export class JSONSchemaFormView extends BoxView {
  private _idPrefix: string;
  private _lastEmitted: any;
  private _form: _schemaform.SchemaForm;
  static _rendermime: IRenderMimeRegistry;

  render() {
    this._idPrefix = `id-wxyz-json-schema-form-${Private.nextId()}`;
    this.pWidget.addClass(FORM_CLASS);
    _dbjrjsf.load().then(() => {
      this.m.on(
        'change:schema change:ui_schema change:value',
        this.rerender,
        this
      );
      this.rerender();
    });
  }

  get m() {
    return this.model as JSONSchemaFormModel;
  }

  get idPrefix() {
    return this._idPrefix;
  }

  async rerender(): Promise<void> {
    const { m, onChange, idPrefix } = this;
    const { SchemaForm } = _dbjrjsf.get();
    const { formData, schema, uiSchema } = m;

    if (!this._form) {
      const { ALL_CUSTOM_UI } = await import(
        '@deathbeds/jupyterlab-rjsf/lib/fields'
      );

      let options = {};

      if (JSONSchemaFormView._rendermime) {
        options = {
          markdown: JSONSchemaFormView._rendermime.createRenderer(
            'text/markdown'
          ) as RenderedMarkdown
        };
      }

      this._form = new SchemaForm(
        schema,
        {
          liveValidate: true,
          formData,
          uiSchema,
          onChange,
          idPrefix,
          ...ALL_CUSTOM_UI
        },
        options
      );
      this._form.addClass(INNER_CLASS);

      this.pWidget.addWidget(this._form);
      return;
    }

    const changed = m.changedAttributes();

    // don't rerender if we just emitted this change
    if (
      changed &&
      changed.value &&
      JSONExt.deepEqual(formData, this._lastEmitted)
    ) {
      return;
    }

    const fm = this._form.model;

    console.log(changed);

    for (const attr of Object.keys(changed)) {
      switch (attr) {
        default:
          break;
        case 'schema':
          fm.schema = schema;
          break;
        case 'ui_schema':
          fm.props = { ...fm.props, uiSchema };
          break;
        case 'value':
          fm.props = { ...fm.props, formData };
          break;
      }
    }
  }

  onChange = (evt: any, _err?: any) => {
    const { m } = this;
    const { formData, errors } = evt;
    if (formData != null) {
      m.errors = errors;
      m.formData = this._lastEmitted = formData;
      this.touch();
    }
  };
}

namespace Private {
  let _nextId = 0;

  export function nextId() {
    return _nextId++;
  }
}
