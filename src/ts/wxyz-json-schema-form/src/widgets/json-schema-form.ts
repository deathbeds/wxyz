import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { JSONExt } from '@lumino/coreutils';

import { DOMWidgetView, DOMWidgetModel } from '@jupyter-widgets/base';

import { lazyLoader } from '@deathbeds/wxyz-core/lib/widgets/lazy';
import { NAME, VERSION } from '..';

const h = React.createElement;

const _rjsf = lazyLoader(
  async () =>
    await import(
      /* webpackChunkName: "react-jsonschema-form" */ 'react-jsonschema-form'
    )
);

const FORM_CLASS = 'jp-WXYZ-JSONSchemaForm';

export class JSONSchemaFormModel extends DOMWidgetModel {
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

export class JSONSchemaFormView extends DOMWidgetView {
  private _idPrefix: string;
  private _lastEmitted: any;

  render() {
    this._idPrefix = `id-wxyz-json-schema-form-${Private.nextId()}`;
    this.pWidget.addClass(FORM_CLASS);
    _rjsf.load().then(() => {
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

  async rerender() {
    const { m, el, onChange, idPrefix } = this;
    const Form = _rjsf.get();
    const { formData, schema, uiSchema } = m;

    const changed = m.changedAttributes();

    // don't rerender if we just emitted this change
    if (
      changed &&
      changed.value &&
      JSONExt.deepEqual(formData, this._lastEmitted)
    ) {
      return;
    }

    ReactDOM.render(
      h(Form.default, {
        schema,
        formData,
        uiSchema,
        onChange,
        idPrefix,
        liveValidate: true
      }),
      el
    );
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
