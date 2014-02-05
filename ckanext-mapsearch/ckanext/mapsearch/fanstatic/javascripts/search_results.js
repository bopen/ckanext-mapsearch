/* global bop, _ */

this.ckan.module('mapsearch-search_results', function ($, _) {
    bop.new_search_results = function () {
        bop.result_nav.update();
        bop.display_search_results();
        bop.update_filter_panel();
    };
    bop.toggle_small_omitted = function () {
      var ele = $('.omitted_small span');
        if (bop.small_extents_are_displayed) {
          bop.hide_small_omitted();
          ele.removeClass("displayed");
          bop.small_extents_are_displayed = false;
        } else {
          bop.show_small_omitted();
          ele.addClass("displayed");
          bop.small_extents_are_displayed = true;
        }
    };
    bop.show_small_omitted = function () {
        $.each(bop.omitted_results.small.results, function (idx, dataset) {
            bop.add_extent_to_map(dataset, {small: true});
        });
    };
    bop.hide_small_omitted = function () {
      bop.result_layer.eachLayer(function (layer) {
        var props = layer.feature.properties;
        if (props.mapsearch && props.mapsearch == 'small') {
            bop.result_layer.removeLayer(layer);
        }
      });
    };
    bop.display_search_results = function () {
        var idx = bop.result_nav.current_page,
            pp = bop.results_per_page,
            to_show = bop.current_results.results.slice(idx * pp, (idx + 1) * pp),
            container = $('#result_panel_container'),
            layer, geoJSON, extents;
        container.find('.dataset_result_panel').remove();
        $('.normal_scale_count span').text(bop.current_results.count);
        bop.result_layer.eachLayer(function (layer) {
            var props = layer.feature.properties;
            if (!props.mapsearch || props.mapsearch != 'small') {
                bop.result_layer.removeLayer(layer);
            };
        });
        $.each(to_show, function (idx, result) {
            bop.add_extent_to_map(result);
            var panel = bop.make_result_panel(result);
            bop.insert_result_panel(panel);
        });
        bop.update_result_list_presentation_mode();
        bop.adjust_result_panel_container_height();
    };

    bop.add_extent_to_map = function (dataset, options) {
        if (dataset.extras && dataset.extras.length > 0) {
            //bop.map.removeLayer(bop.result_layer);
            var extents = ($.grep(dataset.extras,
                    function (extra) {
                        return extra.key === 'spatial';
                    })
                ),
                extent = extents.length > 0 && extents[0];
            if (extent) {
                geoJSON = {"type": "Feature",
                                          "properties": {
                                              "name": dataset.name,
                                              "id": dataset.id
                                          },
                                          "geometry": JSON.parse(extent.value)};
                if (options && options.small) {
                   geoJSON.properties.style = bop.too_small_to_display_style;
                   geoJSON.properties.mapsearch = 'small';
                }
                layer = bop.result_layer.addData(geoJSON);
            }
        }

    };
});
