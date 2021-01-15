// porting https://github.com/openseat/ipylayoutwidgets/blob/master/ipylayoutwidgets/static/ipylayoutwidgets/js/SVGLayoutBoxView.js
/* eslint consistent-this: "off" */
/* eslint @typescript-eslint/no-this-alias: "off" */

import { Widget } from '@lumino/widgets';
import { DOMWidgetModel } from '@jupyter-widgets/base';
import { BoxModel, BoxView } from '@jupyter-widgets/controls';
import { NAME, VERSION } from '../constants';
import * as d3 from 'd3-selection';
import * as d3Zoom from 'd3-zoom';
import _ from 'lodash';
import { JupyterPhosphorPanelWidget } from '@jupyter-widgets/base';

type TDims = {
  height: number;
  width: number;
};

type TZoom = {
  x: number;
  y: number;
  k: number;
};

const CSS = {
  SVG: 'jp-WXYZ-SVG',
  LAYOUT: 'jp-WXYZ-SVG-Layout',
  ZOOM_LOCK: 'jp-WXYZ-SVG-zoom-lock',
  ZOOMER: 'jp-WXYZ-SVG-Zoom',
};

export class SVGBoxModel extends BoxModel {
  static model_name = 'SVGBoxModel';
  static model_module = NAME;
  static model_module_version = VERSION;
  static view_name = 'EditorView';
  static view_module = NAME;
  static view_module_version = VERSION;

  defaults() {
    return {
      ...super.defaults(),
      _model_name: SVGBoxModel.model_name,
      _model_module: NAME,
      _model_module_version: VERSION,
      _view_name: SVGBoxModel.view_name,
      _view_module: NAME,
      _view_module_version: VERSION,
      svg: '<svg></svg>',
      zoom_lock: false,
    };
  }

  private _lastZoom: TZoom;

  saveZoom(zoom: TZoom) {
    const { x, y, k } = this._lastZoom || {};
    if (this._lastZoom && x === zoom.x && y === zoom.y && k == zoom.k) {
      return false;
    }
    this.set({ zoom_x: zoom.x, zoom_y: zoom.y, zoom_k: zoom.k });
    this.save_changes();
    this._lastZoom = zoom;
    return true;
  }
}

class SVGPanelWidget extends JupyterPhosphorPanelWidget {
  onResize(msg: Widget.ResizeMessage) {
    super.onResize(msg);
    (this as any)._view.resize();
  }
}

export class SVGBoxView extends BoxView {
  model: SVGBoxModel;
  private _parser = new DOMParser();
  private _d3: d3.Selection<any, any, any, any>;
  private _lastSVG: string;
  private _original: TDims;
  private _zoomer: d3.Selection<any, any, any, any>;

  _createElement(tagname: string) {
    this.pWidget = new SVGPanelWidget({ view: this });
    return this.pWidget.node;
  }

  initialize(options: any) {
    this._d3 = d3
      .select(this.el)
      .style('position', 'relative')
      .style('text-align', 'center');
    d3.select(window).on('', _.bind(this.update, this));
    this.pWidget.addClass(CSS.SVG);
    this.model.on('change:svg change:area_attr', this.loadSVG, this);
    this.model.on('change:zoom_lock', this.zoomLock, this);
    this.model.on(
      'change:zoom_x change:zoom_y change:zoom_k',
      this.onZoom,
      this
    );
    super.initialize(options);
    this.update(options);
    setTimeout(() => this.resize(), 11);
  }

  zoomLock() {
    if (this.model.get('zoom_lock')) {
      this.pWidget.addClass(CSS.ZOOM_LOCK);
    } else {
      this.pWidget.removeClass(CSS.ZOOM_LOCK);
    }
  }

  onZoom() {
    this._zoomer &&
      this._zoomer.call(
        // TODO: fix this
        this._zoom.transform as any,
        d3Zoom.zoomIdentity
          .translate(this.model.get('zoom_x'), this.model.get('zoom_y'))
          .scale(this.model.get('zoom_k'))
      );
  }

  update(options: any) {
    this.layout();
    super.update(options);
  }

  layout(): void {
    const el = this.el.parentNode;

    if (!el) {
      _.delay(_.bind(this.layout, this), 10);
      return;
    }

    if (this._lastSVG !== this.model.get('svg')) {
      this.loadSVG();
    }

    this.resize();
  }

  addZoom(xml: string) {
    const withZoom = xml
      .replace(/(<svg(.|\n)*?>)/g, `$1\n<g class="${CSS.ZOOMER}">`)
      .replace('</svg>', '</g>\n</svg>');
    return withZoom;
  }

  loadSVG(): void {
    const view = this;
    const el = this.el.parentNode;
    const areaAttr = this.model.get('area_attr');

    this._lastSVG = this.model.get('svg');
    const layout = this._d3.selectAll(CSS.LAYOUT).data([1]);
    layout.remove();
    this._zoom = null;
    layout.enter().call(function () {
      const xml = view._parser.parseFromString(
        view.addZoom(view._lastSVG),
        'image/svg+xml'
      );

      const importedNode = document.importNode(xml.documentElement, true);
      const newLayout = view._d3
        .insert(() => importedNode, ':first-child')
        .classed(CSS.LAYOUT, true);

      view._zoomer = newLayout.select(`.${CSS.ZOOMER}`);

      // find all of the `svg:g`s that are groups
      const children = layout.selectAll('g').filter(
        // tslint:disable
        function () {
          return (
            (this as any).parentNode === newLayout.node() &&
            d3.select(this).attr(`:${areaAttr}`) != null
          );
          // tslint:enable
        }
      );
      const root = layout
        .append('g')
        .attr('id', `${CSS.LAYOUT}-ROOT-${view.cid}`);

      children.each(function () {
        // tslint:disable
        root.node().appendChild(this as any);
        // tslint:enable
      });

      view._original = {
        height: parseInt(newLayout.attr('height'), 10),
        width: parseInt(newLayout.attr('width'), 10),
      };

      layout.attr('width', el.clientWidth).attr('height', el.clientHeight);
    });

    this.resize();
  }

  patternToRegexp(pattern: string): RegExp {
    if (pattern == null) {
      return /.*/;
    }
    try {
      return new RegExp(pattern.replace('.', '\\.').replace('*', '.*'));
    } catch (err) {
      return null;
    }
  }

  private _zoom: d3Zoom.ZoomBehavior<any, any>;

  resize(): void {
    if (!this._original) {
      return;
    }
    const layout = this._d3.select(`.${CSS.LAYOUT}`);

    const view = this;
    if (!this._zoom) {
      this._zoom = d3Zoom.zoom().on('zoom', function ({ transform }) {
        view._zoomer.attr('transform', transform);
        view.model.saveZoom(transform);
      });
      // TODO: fix this
      layout.call(this._zoom as any);
    }
    const el = this.el.parentNode;
    if (!el) {
      return;
    }
    const doc = document.documentElement;
    const aspectRatio = this._original.width / this._original.height;
    const areaWidgets = view.model.get('area_widgets');
    const visibleAreas = this.model
      .get('visible_areas')
      .map(this.patternToRegexp)
      .filter(Object);
    let width = Math.min(el.clientWidth, doc.clientWidth);
    let height = width / aspectRatio;
    let scale = width / this._original.width;
    let labelMap = {} as any;
    let areaAttr = this.model.get('area_attr');

    if (scale * this._original.height > doc.clientHeight) {
      scale = doc.clientHeight / this._original.height;
      height = doc.clientHeight;
      width = height * aspectRatio;
    }
    layout
      .attr('width', width)
      .attr('height', height)
      .style('opacity', this.model.get('show_svg') ? 1 : 0)
      .select(`#${CSS.LAYOUT}-ROOT-${view.cid}`)
      .attr('transform', `scale(${scale})`);
    const area = layout.selectAll('g');
    const named: any = area.filter(function () {
      // tslint:disable
      const label = d3.select(this).attr(`:${areaAttr}`);
      // tslint:enable
      return label && visibleAreas.find((re: any) => label.match(re));
    });

    area.each(function () {
      // tslint:disable
      const area = this;
      // tslint:enable
      const el = d3.select(area);
      const label = el.attr(`:${areaAttr}`);
      const visible =
        named._groups.indexOf(area) > -1 ||
        _.some(named._groups[0], (child: any) => (area as any).contains(child));

      if (label && visible) {
        labelMap[label] = area;
      }

      el.style('display', visible ? 'inline' : 'none');
    });

    const el_bb = view.el.getBoundingClientRect();
    const childModels: DOMWidgetModel[] = view.model.get('children');

    _(areaWidgets).forIn(function (idx, label) {
      const item = childModels[idx];
      let labelRegExp = view.patternToRegexp(label);
      if (!labelRegExp) {
        return;
      }
      const area = _(labelMap).find((_area: any, areaLabel: any) =>
        areaLabel.match(labelRegExp)
      );
      const bb = area && area.getBoundingClientRect();

      if (!area) {
        _(item.views).forIn(function (childPromise) {
          childPromise
            .then((child: any) => {
              d3.select(child.el).style('display', 'none');
            })
            .catch(console.warn);
        });
        return;
      }

      ['width', 'height'].map(function (attr) {
        if (!item.has(attr)) {
          return;
        }
        item.set(attr, bb[attr]);
      });

      _(item.views).forIn(function (child) {
        child
          .then(function (child: any) {
            d3.select(child.el)
              .style('position', 'absolute')
              .style('display', null)
              .style('opacity', 1.0)
              .style('top', `${bb.top - el_bb.top}px`)
              .style('left', `${bb.left - el_bb.left}px`)
              .style('width', `${bb.width}px`)
              .style('height', `${bb.height}px`);
            child.touch();
          })
          .catch(console.warn);
      });
    });
  }
}
