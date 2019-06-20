import * as core from '@deathbeds/wxyz-core';
import * as datagrid from '@deathbeds/wxyz-datagrid';
import * as html from '@deathbeds/wxyz-html';
import * as iiif from '@deathbeds/wxyz-iiif';
import * as jsonld from '@deathbeds/wxyz-jsonld';
import * as lab from '@deathbeds/wxyz-lab';
import * as svg from '@deathbeds/wxyz-svg';
import * as tplNunjucks from '@deathbeds/wxyz-tpl-nunjucks';
import * as yaml from '@deathbeds/wxyz-yaml';

const DEBUG = false;

if (DEBUG) {
  console.log(core, datagrid, html, jsonld, lab, svg, tplNunjucks, yaml, iiif);
}
