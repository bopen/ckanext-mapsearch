var bop;

this.ckan.module('mapsearch-geofacets', function ($, _) {
    bop.extract_geofacet = function (q) {
        return q.match(/geo:[^ ]+/);
    }
    // looks up a geoname, sets the map to the first entry and puts
    // alternatives in their panel (if there are alternatives)
    bop.geolookup_name = function (name) {
        var panel = $('#geo_alternative_panel'),
            url = "http://nominatim.openstreetmap.org/search",
            params= {q: name, format: 'json', addressdetails: 0, polygon_json:1};
        bop.during_geolookup = true;
        $.get(url, params,
            function (res) {
                var bb;
                res = res.filter(function (entry) {
                    return ((entry.class === 'boundary' || entry.class === 'place')
                             && entry.boundingbox);
                });
                // remove 'place' if 'boundary' of the same entity is present
                res = res.filter(
                    function (entry) {
                        var homonyms =  res.filter(
                            function(inner) {
                                return inner.display_name === entry.display_name
                            }
                        );
                        return homonyms.length == 1 || homonyms.length > 1 && entry.class === 'boundary';
                });
                panel.hide();
                if (res.length > 0) {
                    bb = res[0].boundingbox;
                    bop.map.fitBounds([[bb[0], bb[2]], [bb[1], bb[3]]]);
                    if (res.length > 1) {
                        var list = panel.find('ul'),
                            proto = $('<li>'),
                            link = $('<a>');
                        panel.show();
                        link.attr('href', 'javascript:void(0)');
                        proto.append(link);
                        list.children().remove();
                        res.forEach(function (entry) {
                            var item = proto.clone(),
                                bb = entry.boundingbox;
                            link = item.find('a');
                            link.text(entry.display_name);
                            link.on('click', function () {
                                bop.map.fitBounds([[bb[0], bb[2]], [bb[1], bb[3]]]);
                            });
                            list.append(item);
                        });
                    }
                }
                bop.during_geolookup = false;
                bop.map.fireEvent('moveend');
            }
        );
    }
});
