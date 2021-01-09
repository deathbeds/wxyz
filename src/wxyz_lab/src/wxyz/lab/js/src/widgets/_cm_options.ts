import * as CodeMirror from 'codemirror';

type TJSONUnsafeOption =
  | 'extraKeys'
  | 'lineNumberFormatter'
  | 'onDragEvent'
  | 'onKeyEvent'
  | 'lint'
  | 'value';

type TJSONSafeConfig = Omit<CodeMirror.EditorConfiguration, TJSONUnsafeOption>;

interface IHasName {
  name: string;
}

export interface IEditorConfiguration extends TJSONSafeConfig {
  /**
   * string|object. The mode to use. When not given, this will default to
   * the first mode that was loaded. It may be a string, which either simply names
   * the mode or is a MIME type associated with the mode. Alternatively, it may be
   * an object containing configuration options for the mode, with a name property
   * that names the mode (for example {name: "javascript", json: true}).
   */
  mode: string | (IHasName & Record<string, unknown>);
  readOnly: boolean | 'nocursor';
}
