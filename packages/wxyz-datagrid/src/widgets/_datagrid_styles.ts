import { DataGrid } from '@lumino/datagrid';

export type TJSONUnsafeStyle = 'rowBackgroundColor' | 'columnBackgroundColor';

export type TJSONSafeStyles = Omit<DataGrid.Style, TJSONUnsafeStyle>;

export interface IDataGridStyles extends TJSONSafeStyles {
  /**
   * Realized as a functor, a single value will affect all rows, while any
   * other value will be return modulo the position.
   */
  rowBackgroundColor: string[];

  /**
   * @see rowBackgroundColor
   */
  columnBackgroundColor: string[];
}
