import { TObject } from '@deathbeds/wxyz-core/src/widgets/_base';

declare module 'jsonld' {
  export function compact<T = TObject>(
    doc: any,
    context: IContext,
    options: ICompactOptions
  ): Promise<T>;

  export function expand<T = TObject>(
    doc: any,
    options: IExpandOptions
  ): Promise<T[]>;

  export function flatten<T = TObject>(
    doc: any,
    context: IContext,
    options: IExpandOptions
  ): Promise<T>;

  export function frame<T = TObject>(
    doc: any,
    frame: IContext,
    options: IExpandOptions
  ): Promise<T>;

  export function normalize<T = TObject | string>(
    doc: any,
    options: INormalizeOptions
  ): Promise<T>;

  export interface IStaticContext {
    [key: string]: any;
  }
  export interface IContext {
    '@context': string | IStaticContext | (string | IStaticContext)[];
  }

  export interface ICompactOptions extends IExpandOptions {
    /*
     * @param [options] options to use:
     *          [framing] true if compaction is occuring during a framing operation.
     * @param [callback(err, compacted)] called once the operation completes.
     */
    /** the base IRI to use */
    base?: string;
    /** true to compact arrays to single values when appropriate, false not to (default: true). */
    compactArrays?: boolean;
    /** true to compact IRIs to be relative to document base, false to keep absolute (default: true) */
    compactToRelative?: boolean;
    /** true to always output a top-level graph (default: false). */
    graph?: boolean;
    /** true to assume the input is expanded and skip expansion, false not to, defaults to false. */
    skipExpansion?: boolean;
    /** true if compaction is occuring during a framing operation. */
    framing?: boolean;
    /** instead of references, create a (potentially-circular) JSON object */
    link?: boolean;
    // TODO // documentLoader: IDocumentLoader;
    //  [documentLoader(url, callback(err, remoteDoc))] the document loader.
    /* TODO // expansionMap: IExpansionMap;
    /** [expansionMap(info)] a function that can be used to custom map
     *            unmappable values (or to throw an error when they are detected);
     *            if this function returns `undefined` then the default behavior
     *            will be used. */
    /* TODO // compactionMap: ICompactionMap;
     *          [compactionMap(info)] a function that can be used to custom map
     *            unmappable values (or to throw an error when they are detected);
     *            if this function returns `undefined` then the default behavior
     *            will be used. */
    // issuer: new IdentifierIssuer('_:b')
  }

  export interface IExpandOptions {
    /** a context to expand with. */
    expandContext?: IContext;
  }

  export interface INormalizeOptions extends IExpandOptions {
    format?: string;
  }
}
