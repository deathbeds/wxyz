import screenfull from 'screenfull';

import { Platform } from '@lumino/domutils';

import { BoxModel, BoxView } from '@jupyter-widgets/controls';

import { NAME, VERSION } from '../constants';

const FULL_CLASS = 'jp-WXYZ-Fullscreen';

export class FullscreenModel extends BoxModel {
  static model_name = 'FullscreenModel';
  static model_module = NAME;
  static model_module_version = VERSION;
  static view_name = 'FullscreenView';
  static view_module = NAME;
  static view_module_version = VERSION;

  defaults() {
    return {
      ...super.defaults(),
      _model_name: FullscreenModel.model_name,
      _model_module: NAME,
      _model_module_version: VERSION,
      _view_name: FullscreenModel.view_name,
      _view_module: NAME,
      _view_module_version: VERSION,
    };
  }
}

export class FullscreenView extends BoxView {
  initialize(options: any) {
    super.initialize(options);
    this.pWidget.addClass(FULL_CLASS);
  }
  events() {
    return {
      click: async (evt: any) => {
        const mouseEvent = evt as MouseEvent;
        if (Platform.accelKey(mouseEvent) && mouseEvent.shiftKey) {
          if (screenfull && screenfull.isEnabled) {
            await screenfull.request(this.el);
          }
        }
      },
    };
  }
}
