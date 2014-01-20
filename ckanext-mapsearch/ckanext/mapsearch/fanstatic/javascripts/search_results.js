/* global bop, _ */

this.ckan.module('mapsearch-search_results', function ($, _) {
    bop.display_search_results = function (results) {
        var layer, geoJSON;
        var container = $('#result_panel_container');
        container.empty();
        bop.result_layer.eachLayer(function (layer) {
            bop.result_layer.removeLayer(layer);
        });
        $.each(results, function (idx, result) {
            if (result.extras && result.extras.length > 0) {
                //bop.map.removeLayer(bop.result_layer);
                extents = ($.grep(result.extras,
                    function (extra, idx) {
                        return extra.key == 'spatial';
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
