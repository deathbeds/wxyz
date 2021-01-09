import { CellRenderer, TextRenderer } from '@lumino/datagrid';

import { unpack_models as deserialize } from '@jupyter-widgets/base';

import { WXYZ } from '@deathbeds/wxyz-core/lib/widgets/_base';

export interface IChildChangedFunc {
  (): void;
}

export class CellRendererModel extends WXYZ {
  static model_name = 'CellRendererModel';

  // todo: some default for onChildChanged for the linter and docs
  toRenderer(_?: IChildChangedFunc): CellRenderer {
    return null;
  }
}

export class FormatFuncModel extends WXYZ {
  static model_name = 'FormatFuncModel';

  toFormatFunc(): TextRenderer.FormatFunc {
    return null;
  }
}

export class FixedFuncModel extends FormatFuncModel {
  static model_name = 'FixedFuncModel';

  toFormatFunc() {
    return TextRenderer.formatFixed({
      digits: this.get('digits'),
      missing: this.get('missing'),
    });
  }
}

export class TextRendererModel extends CellRendererModel {
  static model_name = 'TextRendererModel';

  static serializers = {
    ...CellRendererModel.serializers,
    format_func: { deserialize },
  };

  toRenderer(onChildChanged?: IChildChangedFunc): TextRenderer {
    let formatFunc: FormatFuncModel;

    try {
      formatFunc = this.get('format_func');
      onChildChanged && formatFunc.on('change', () => onChildChanged());
    } catch {
      // TODO: something reasonable
    }

    return new TextRenderer({
      textColor: () => this.get('text_color'),
      backgroundColor: () => this.get('background_color') || '',
      format: formatFunc ? formatFunc.toFormatFunc() : null,
      horizontalAlignment: () => this.get('horizontal_alignment'),
      verticalAlignment: () => this.get('vertical_alignment'),
      font: () => this.get('font'),
    });
  }
}
