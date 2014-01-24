/* global bop, _ */

this.ckan.module('mapsearch-search_results', function ($, _) {
    bop.new_search_results = function () {
        bop.result_nav.update();
        bop.display_search_results();
        bop.update_filter_panel();
    };
    bop.show_small_omitted = function () {
        $.each(bop.omitted_results.small.results, function (idx, dataset) {
            bop.add_extent_to_map(dataset);
        });
    };
    bop.display_search_results = function () {
        var idx = bop.result_nav.current_page,
            pp = bop.results_per_page,
            to_show = bop.current_results.slice(idx * pp, (idx + 1) * pp),
            container = $('#result_panel_container'),
            layer, geoJSON, extents;
        container.find('.dataset_result_panel').remove();
        bop.result_layer.eachLayer(function (layer) {
            bop.result_layer.removeLayer(layer);
        });
        $.each(to_show, function (idx, result) {
            bop.add_extent_to_map(result);
            var panel = bop.make_result_panel(result);
            bop.insert_result_panel(panel);
        });
        bop.update_result_list_presentation_mode();
        bop.adjust_result_panel_container_height();
    };
});

bop.add_extent_to_map = function (dataset) {
    if (dataset.extras && dataset.extras.length > 0) {
        //bop.map.removeLayer(bop.result_layer);
        extents = ($.grep(dataset.extras,
            function (extra) {
                return extra.key === 'spatial';
            })
          );
        extent = extents.length > 0 && extents[0];
        if (extent) {
            geoJSON = {"type": "Feature",
                                      "properties": {
                                          "name": dataset.name,
                                          "id": dataset.id
                                      },
                                      "geometry": JSON.parse(extent.value)};
            layer = bop.result_layer.addData(geoJSON);
        }
    }

};
