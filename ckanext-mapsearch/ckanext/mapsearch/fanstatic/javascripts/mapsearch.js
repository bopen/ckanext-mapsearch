/* Module for handling the strictly map-related functionality
 */
this.ckan.module('mapsearch', function ($, _) {

  return {
    options: {
      i18n: {
      },
      style: {
        color: '#F06F64',
        weight: 2,
        opacity: 1,
        fillColor: '#F06F64',
        fillOpacity: 0.1
      },
      default_extent: [[49, 20], [40, 5]]
    },
    template: {
      buttons: [
        '<div id="dataset-map-edit-buttons">',
        '<a href="javascript:;" class="btn cancel">Cancel</a> ',
        '<a href="javascript:;" class="btn apply disabled">Apply</a>',
        '</div>'
      ].join('')
    },

    initialize: function () {
      var module = this;
      $.proxyAll(this, /_on/);

      var user_default_extent = this.el.data('default_extent');
      if (user_default_extent ){
        if (user_default_extent instanceof Array) {
          // Assume it's a pair of coords like [[90, 180], [-90, -180]]
          this.options.default_extent = user_default_extent;
        } else if (user_default_extent instanceof Object) {
          // Assume it's a GeoJSON bbox
          this.options.default_extent = new L.GeoJSON(user_default_extent).getBounds();
        }
      }
      this.el.ready(this._onReady);
    },

    _getParameterByName: function (name) {
      var match = RegExp('[?&]' + name + '=([^&]*)')
                        .exec(window.location.search);
      return match ?
          decodeURIComponent(match[1].replace(/\+/g, ' '))
          : null;
    },

    _drawExtentFromCoords: function(xmin, ymin, xmax, ymax) {
        if ($.isArray(xmin)) {
            var coords = xmin;
            xmin = coords[0]; ymin = coords[1]; xmax = coords[2]; ymax = coords[3];
        }
        return new L.Rectangle([[ymin, xmin], [ymax, xmax]],
                               this.options.style);
    },

    _drawExtentFromGeoJSON: function(geom) {
        return new L.GeoJSON(geom, {style: this.options.style});
    },

    _onReady: function() {
      var module = this;
      var map;
      var extentLayer;
      var previous_box;
      var previous_extent;
      var is_exanded = true;
      var should_zoom = true;
      var form = $("#dataset-search");
      var move_counter = 0;
      // CKAN 2.1
      if (!form.length) {
          form = $(".search-form");
      }

      var buttons;

      // Add necessary fields to the search form if not already created
      $(['ext_bbox', 'ext_prev_extent']).each(function(index, item){
        if ($("#" + item).length === 0) {
          $('<input type="hidden" />').attr({'id': item, 'name': item}).appendTo(form);
        }
      });

      // OK map time
      map = ckan.commonLeafletMap('map-container', this.options.map_config, {attributionControl: false});

      map.addControl(new L.Control.Scale({imperial:false, maxWidth: 200}));

      // Initialize the draw control
      map.addControl(new L.Control.Draw({
        position: 'topright',
        polyline: false, polygon: false,
        circle: false, marker: false,
        rectangle: {
          shapeOptions: module.options.style,
          title: 'Draw rectangle'
        },
      }));
      var onEachFeature = function  (feature, layer) {
          if (feature.properties.mapsearch && feature.properties.mapsearch == 'small') {
              return;
          };
          if (feature.properties && feature.properties.id) {
              layer.on({'click':
                  function () {
                      bop.select_result(feature.properties.id);
                  },
              });
          }
      };

      if (typeof bop !== 'undefined') {
          bop.map = map;
          bop.result_layer = L.geoJson([], {
            onEachFeature:onEachFeature,
            style: function (feature) {
                if (feature && feature.properties && feature.properties.style) {
                    return feature.properties.style;
                } else {
                    return bop.result_style;
                }
            }
          }).addTo(map);
      }

      map.on('moveend', function (e) {
          if (!extentLayer) {
              $('#ext_bbox').val(map.getBounds().toBBoxString());
              if (move_counter > 0) {
                  //console.log("requesting datasets");
                  bop.request_datasets();
              }
          }
          move_counter++;
          $('#ext_prev_extent').val(map.getBounds().toBBoxString());
      });

      // When user finishes drawing the box, record it and add it to the map
      map.on('draw:rectangle-created', function (e) {
        if (extentLayer) {
            map.removeLayer(extentLayer);
        }
        extentLayer = e.rect;
        bop.extentLayer = extentLayer;
        $('#ext_bbox').val(extentLayer.getBounds().toBBoxString());
        map.addLayer(extentLayer);
        bop.request_datasets();
        $('.apply', buttons).removeClass('disabled').addClass('btn-primary');
      });

      map.fitBounds(module.options.default_extent);
    }
  }
});
