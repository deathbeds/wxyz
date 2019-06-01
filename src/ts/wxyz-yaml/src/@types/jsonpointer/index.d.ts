declare module 'jsonpointer' {
  export interface JSONPointer {
    /**
     * Looks up a JSON pointer in an object
     */
    get(object: Object, pointer: string): any;

    /**
     * Set a value for a JSON pointer on object
     */
    set(object: Object, pointer: string, value: any): void;
  }
  /**
   * Looks up a JSON pointer in an object
   */
  export function get(object: Object, pointer: string): any;

  /**
   * Set a value for a JSON pointer on object
   */
  export function set(object: Object, pointer: string, value: any): void;

  /**
   *  Builds a JSONPointer instance from a pointer value.
   */
  export function compile(pointer: string): JSONPointer;
}
