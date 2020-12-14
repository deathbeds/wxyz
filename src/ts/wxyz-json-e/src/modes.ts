import CodeMirror from 'codemirror';
import 'codemirror/mode/yaml/yaml';

const RE_OP0 = /(then|else|from|each\([^)]+\))(?=:)/;
const RE_OP1 = /\$(flattenDeep|mergeDeep)/;
const RE_OP2 = /\$(eval|json|if|then|else|flatten|fromNow|let|map|match|merge|sort|switch|reverse)(?=:)/;
const RE_EX = /\$\{[^\}]*\}/;
const RE_END = /\$|(then|else|from|each\(.*\)):/;

const T = {
  BUILT_IN: 'variable-2',
  MOD: 'variable-3',
  EXPR: 'variable-2'
};

function yamlEMode(config: any, parserConfig: any) {
  const yamlEOverlay = {
    token: function(stream: any, _state: any) {
      if (stream.match(RE_OP0)) {
        return T.MOD;
      }
      if (stream.match(RE_OP1) || stream.match(RE_OP2)) {
        return T.BUILT_IN;
      }
      if (stream.match(RE_EX)) {
        return T.EXPR;
      }
      while (true) {
        if (stream.next() == null || stream.match(RE_END, false)) {
          break;
        }
      }
      return null;
    }
  };

  return CodeMirror.overlayMode(
    CodeMirror.getMode(config, parserConfig.backdrop || 'text/yaml'),
    yamlEOverlay
  );
}

CodeMirror.defineMode('yaml-e', yamlEMode);
