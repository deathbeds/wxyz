import * as core from '@deathbeds/wxyz-core';
import * as datagrid from '@deathbeds/wxyz-datagrid';
import * as html from '@deathbeds/wxyz-html';
import * as jsonld from '@deathbeds/wxyz-jsonld';
import * as lab from '@deathbeds/wxyz-lab';
import * as svg from '@deathbeds/wxyz-svg';
import * as tplNunjucks from '@deathbeds/wxyz-tpl-nunjucks';
import * as yaml from '@deathbeds/wxyz-yaml';
import * as jsonSchemaForm from '@deathbeds/wxyz-json-schema-form';
import * as dvcs from '@deathbeds/wxyz-dvcs';

const DEBUG = false;

if (DEBUG) {
  console.log(
    core,
    datagrid,
    dvcs,
    html,
    jsonld,
    jsonSchemaForm,
    lab,
    svg,
    tplNunjucks,
    yaml
  );
}
