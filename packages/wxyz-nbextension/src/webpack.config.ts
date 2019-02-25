import * as path from 'path';
import * as webpack from 'webpack';

const externals = ['@jupyter-widgets/base'];

const pySrc = path.resolve(__dirname, '..', '..', 'ipywxyz', 'src', 'ipywxyz');

const output: Partial<webpack.Output> = {
  filename: 'index.js',
  libraryTarget: 'amd'
};

const nbextension: webpack.Configuration = {
  devtool: 'source-map',
  entry: './lib/index.js',
  mode: 'production',
  module: {
    rules: [
      { test: /\.js$/, use: ['source-map-loader'], enforce: 'pre' },
      { test: /\.css$/, use: ['style-loader', 'css-loader'] }
    ]
  },
  output: { path: path.resolve(pySrc, 'static', 'wxyz'), ...output },
  externals
};

const bundle: webpack.Configuration = {
  ...nbextension,
  output: {
    path: path.resolve(__dirname, 'dist'),
    library: '@deathbeds/jupyterlab-wxyz',
    publicPath: `https://deathbeds.github.io/wxyz/wxyz-nbextextension@0.1.0/dist/`,
    ...output
  }
};

export default [nbextension, bundle];
