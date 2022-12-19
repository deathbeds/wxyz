import { PromiseDelegate } from '@lumino/coreutils';

export function lazyLoader<T>(loader: () => Promise<T>) {
  let _lib: T;
  let _promiseDelegate: PromiseDelegate<T>;

  function get() {
    return _lib;
  }

  async function load() {
    if (_lib) {
      return _lib;
    }
    if (_promiseDelegate) {
      return await _promiseDelegate.promise;
    }
    _promiseDelegate = new PromiseDelegate();
    _lib = await loader();
    _promiseDelegate.resolve(_lib);
  }

  return { get, load };
}
