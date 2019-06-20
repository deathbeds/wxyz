import { BoxView } from '@jupyter-widgets/controls';
import { unpack_models as deserialize } from '@jupyter-widgets/base';

import { IMirador, Mirador } from 'mirador';

import { lazyLoader } from '@deathbeds/wxyz-core/lib/widgets/lazy';
import { WXYZ, WXYZBox } from '@deathbeds/wxyz-core/lib/widgets/_base';

import { NAME, VERSION } from '..';

const _mirador = lazyLoader(
  async () => await import(/* webpackChunkName: "mirador" */ 'mirador')
);

export class ManifestModel extends WXYZ {
  static model_name = 'ManifestModel';
  static model_module = NAME;
  static model_module_version = NAME;
  static view_module = VERSION;
  static view_module_version = VERSION;
  defaults() {
    return {
      ...super.defaults(),
      _model_name: IIIFModel.model_name,
      _view_name: IIIFModel.view_name,
      _model_module: NAME,
      _model_module_version: VERSION,
      _view_module: NAME,
      _view_module_version: VERSION,
      url: ''
    };
  }
}

export class IIIFModel extends WXYZBox {
  static model_name = 'IIIFModel';
  static view_name = 'IIIFView';
  static model_module = NAME;
  static model_module_version = NAME;
  static view_module = VERSION;
  static view_module_version = VERSION;
  static serializers = { ...WXYZBox.serializers, manifests: { deserialize } };

  defaults() {
    return {
      ...super.defaults(),
      _model_name: IIIFModel.model_name,
      _view_name: IIIFModel.view_name,
      _model_module: NAME,
      _model_module_version: VERSION,
      _view_module: NAME,
      _view_module_version: VERSION,
      manifests: []
    };
  }
}

export class IIIFView extends BoxView {
  private _elMirador: HTMLElement;
  private _viewer: Mirador.IViewer;
  initialize(parameters: any) {
    super.initialize(parameters);
    const id = `id-iiif-${Private.nextId()}`;
    this._elMirador = document.createElement('div');
    this._elMirador.id = id;
    (this.el as HTMLElement).appendChild(this._elMirador);
    this.model.on('change:manifests', this.onManifests, this);
    this.onManifests();
  }

  private _manifestInterval: number;

  onManifests() {
    if (!this._viewer && this._manifestInterval == null) {
      this._manifestInterval = setInterval(() => {
        if (!this._viewer) {
          return;
        }
        clearInterval(this._manifestInterval);
        this.onManifests();
      }, 100);
      return;
    }
    let manifests = this.model.get('manifests') as ManifestModel[];
    let { store, actions } = this._viewer;
    manifests.forEach(m => {
      let manifestId = m.get('url');
      store.dispatch(actions.addWindow({ manifestId }));
    });
  }

  render() {
    if (this._viewer == null) {
      setTimeout(async () => {
        await _mirador.load();
        const mirador = _mirador.get();
        console.log(mirador);
        const viewer = ((mirador as any) as IMirador).viewer({
          id: this._elMirador.id
        } as any);
        console.log('VIEWER', viewer);
        this._viewer = viewer;
        viewer.store.subscribe(() => this.onState());
      }, 1);
      return;
    }
  }

  onState() {
    const { store } = this._viewer;
    let state = store.getState();
    let stateManifests = state.manifests;
    let modelManifests = this.model.get('manifests');
    let modelManifestMap = modelManifests.reduce(
      (memo: any, manifest: ManifestModel) => {
        memo[manifest.get('url')] = manifest;
        return memo;
      },
      {}
    );
    Object.keys(stateManifests).forEach(id => {
      if (!modelManifestMap[id]) {
        console.log('missing a model', id);
      } else {
        let stM = stateManifests[id];
        let mM = modelManifestMap[id];
        let { error, json, isFetching } = stM;
        mM.set({
          error: error || '',
          value: json || {},
          fetching: isFetching || false
        });
        mM.save_changes();
      }
    });
  }
}

namespace Private {
  let _nextId = 0;

  export function nextId() {
    return _nextId++;
  }
}
