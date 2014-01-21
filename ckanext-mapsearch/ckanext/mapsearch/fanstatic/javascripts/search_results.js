/* global bop, _ */

this.ckan.module('mapsearch-search_results', function ($, _) {
    bop.new_search_results = function () {
        bop.result_nav.update();
        bop.display_search_results();
    };
    bop.display_search_results = function () {
        var idx = bop.result_nav.current_page,
            pp = bop.results_per_page,
            to_show = bop.current_results.slice(idx * pp, (idx + 1) * pp),
            container = $('#result_panel_container'),
            layer, geoJSON, extents;
        container.empty();
        bop.result_layer.eachLayer(function (layer) {
            bop.result_layer.removeLayer(layer);
        });
        $.each(to_show, function (idx, result) {
            if (result.extras && result.extras.length > 0) {
                //bop.map.removeLayer(bop.result_layer);
                extents = ($.grep(result.extras,
                    function (extra) {
                        return extra.key === 'spatial';
                    })
                  );
                extent = extents.length > 0 && extents[0];
                if (extent) {
                    geoJSON = {"type": "Feature",
                                              "properties": {
                                                  "name": result.name,
                                                  "id": result.id
                                              },
                                              "geometry": JSON.parse(extent.value)};
                    layer = bop.result_layer.addData(geoJSON);
                }
            }
            var panel = bop.make_result_panel(result);
            bop.insert_result_panel(panel);
        });
        bop.update_result_list_presentation_mode();
    };
});
