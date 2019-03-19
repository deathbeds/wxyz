// porting https://github.com/openseat/ipylayoutwidgets/blob/master/ipylayoutwidgets/static/ipylayoutwidgets/js/SVGLayoutBoxView.js

import { BoxModel, BoxView } from '@jupyter-widgets/controls';
import { NAME, VERSION } from '..';
import * as d3 from 'd3-selection';
import _ from 'lodash';

const SVG_CLASS = 'jp-WXYZ-SVG';

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
      svg: '<svg></svg>'
    };
  }
}

export class SVGBoxView extends BoxView {
  private _parser = new DOMParser();
  private _d3: d3.Selection<any, any, any, any>;
  private _lastSVG: string;

  initialize() {
    this._d3 = d3
      .select(this.el)
      .style('position', 'relative')
      .style('text-align', 'center');
    d3.select(window).on('resize', _.bind(this.update, this));
    console.log(this._d3, this._parser);
    // //
    this.model.on('change:svg', _.bind(this.loadSVG, this));
    // //
    // // SVGLayoutBoxView.__super__.initialize.apply(this, arguments);
    // //
    // // this.update();
  }

  loadSVG() {
    console.log('load', this.model.get('svg'));
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
  //
  // load_svg: function(){
  //   var view = this,
  //     el = this.el.parentNode;
  //
  //   view.last_layout = this.model.get("svg");
  //
  //   var layout = this.d3.selectAll(".ipnbdbtk-svg-layout").data([1])
  //   layout.remove();
  //   layout.enter()
  //     .call(function(){
  //       var xml = view.parser.parseFromString(view.last_layout, "image/svg+xml"),
  //         importedNode = document.importNode(xml.documentElement, true),
  //         layout = view.d3.insert(
  //             function(){return importedNode; },
  //             ":first-child"
  //           )
  //           .classed({"ipnbdbtk-svg-layout": 1})
  //           .style({
  //             "z-index": -1
  //           });
  //
  //         // find all of the `svg:g`s that are groups
  //         var children = layout.selectAll("g").filter(function(){
  //           return this.parentNode === layout.node() &&
  //             d3.select(this).attr("inkscape:groupmode") === "layer";
  //         });
  //
  //         var root = layout.append("g").attr("id", "ROOT-"+ view.cid);
  //
  //         children.each(function(){ root.node().appendChild(this); });
  //
  //         view.original = {
  //           height: parseInt(layout.attr("height")),
  //           width: parseInt(layout.attr("width")),
  //         };
  //
  //         layout.attr({
  //           width: el.clientWidth,
  //           height: el.clientHeight,
  //         });
  //     });
  // },
  //
  // patternToRegexp: function(pattern){
  //   return new RegExp(
  //     pattern
  //       .replace(".", "\\.")
  //       .replace("*", ".*")
  //   )
  // },
  //
  resize(): void {
    const layout = this._d3.select(SVG_CLASS);
    console.log('resize', layout);
    // const el = this.el.parentNode;
    // const doc = document.documentElement;
    // const aspectRatio = this.original.width / this.original.height;
    //   width = Math.min(el.clientWidth, doc.clientWidth),
    //   height = width / aspect_ratio,
    //   label_map = {},
    //   visible_layers = this.model.get("visible_layers")
    //     .map(this.patternToRegexp),
    //   scale = width / this.original.width;
    //
    //   if(scale * this.original.height > doc.clientHeight){
    //     scale = doc.clientHeight / this.original.height;
    //     height = doc.clientHeight;
    //     width = height * aspect_ratio;
    //   }
    //
    //   layout.attr({
    //       width: width,
    //       height: height
    //     })
    //     .style({
    //       opacity: this.model.get("show_svg") ? 1 : 0
    //     })
    //     .select("#ROOT-"+ view.cid)
    //     .attr({
    //       transform: "scale(" + scale + ")"
    //     });
    //
    //   var layer = layout.selectAll("g"),
    //     named = layer.filter(function(){
    //       var label = d3.select(this).attr("inkscape:label");
    //
    //       return label && visible_layers.find(function(visible_re){
    //         return label.match(visible_re);
    //       });
    //     });
    //
    //   layer.each(function(){
    //     var layer = this,
    //       el = d3.select(this),
    //       label = el.attr("inkscape:label"),
    //       visible = named[0].indexOf(layer) > -1 ||
    //         _.any(named[0], function(child){ return layer.contains(child); });
    //
    //     if(label && visible){
    //       label_map[label] = this;
    //     }
    //
    //     el.style({
    //       display: visible ? "inline" : "none"
    //     });
    //   });
    //
    //   var el_bb = view.el.getBoundingClientRect();
    //
    //   _(view.model.get("widget_map"))
    //     .map(function(item, label){
    //       var label_re = view.patternToRegexp(label),
    //           layer = _(label_map).find(function(layer, layer_label){
    //             return layer_label.match(label_re);
    //           }),
    //           bb = layer && layer.getBoundingClientRect(),
    //           changed = false;
    //
    //       if(!layer){
    //         _(item.views).map(function(child){
    //           child.then(function(child){
    //             d3.select(child.el)
    //               .transition()
    //               .style({opacity: 0})
    //               .transition().style({display: "none"});
    //           })
    //         });
    //
    //         return;
    //       }
    //
    //       ["width", "height"].map(function(attr){
    //         if(!item.has(attr)){ return; }
    //         item.set(attr, bb[attr]);
    //         changed = true;
    //       });
    //
    //       _(item.views).map(function(child){
    //         child.then(function(child){
    //           d3.select(child.el)
    //             .transition()
    //             .style({
    //               position: "absolute",
    //               display: "block",
    //               opacity: 1.0,
    //               top: (bb.top - el_bb.top) + "px",
    //               left: (bb.left - el_bb.left) + "px",
    //               width: bb.width + "px",
    //               height: bb.height + "px"
    //             });
    //           child.touch();
    //         })
    //       });
    //     });
  }
}
