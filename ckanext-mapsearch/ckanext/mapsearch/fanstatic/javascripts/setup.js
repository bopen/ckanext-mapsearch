this.ckan.module('mapsearch-setup', function ($, _) {
    if (typeof bop === 'undefined') {bop = {}};

    $(document).ready(function () {
        bop.resizeDiv();
        bop.result_style = {
            color: '#2F2FFF',
            weight: 1,
            opacity: 1,
            fillColor: '#2F2FFF',
            fillOpacity: 0.1
          };
        bop.too_small_to_display_style = $.extend({}, bop.result_style,
                                                     {fillColor: '#DDDD99',
                                                       fillOpacity: 0.499});
        bop.highlightStyle = $.extend({}, bop.result_style,
                                                {fillColor: '#FFFFFF',
                                                 fillOpacity: 0.499});

        $('#keyword_search_input').autocomplete({
           delay: 500,
           close: bop.request_datasets,
           source: function(current, display_response) {
               bop.request_completion(display_response);
           },
           minLength: 2,
        });

        $('#keyword_search_input').keypress(function( event ) {
            if (event.which == 13) {
                event.preventDefault();
                var q = $('#keyword_search_input').val(),
                    geofacets = bop.extract_geofacet(q),
                    geofacet = geofacets &&  geofacets.length && geofacets[0];
                if (geofacet) {
                   bop.geolookup_name(geofacet.split(":")[1]);
                }
                $("#keyword_search_input").autocomplete("close");
                bop.request_datasets();
            }
        });

        $('#keyword_clear_button').click(function( event ) {
            if (bop.extentLayer) {
                bop.map.removeLayer(bop.extentLayer);
                delete bop.extentLayer;
                $('#ext_bbox').val(bop.map.getBounds().toBBoxString());
            }
            $('#keyword_search_input').val("");
            bop.filters = [];
            $('#filter_panel').hide();
            bop.request_datasets();
        });

        bop.setup_filter_panel();
        bop.result_nav.setup();
        if (bop.query_on_load) {
            setTimeout(function () {
                           bop.map.fireEvent('moveend');
            }, 500);
        }

        $('#filter_help_window').dialog({
            autoOpen:false, modal:false,
            title:"Faceted Search", buttons: [{
                text: "OK", click: function() {$( this ).dialog( "close" ); }}],
            width:'66%'});

        $('#filter_help_opener').click(function (event) {
            $('#filter_help_window').dialog("open");
            event.preventDefault();
            return false;
        });

        $('#scale_toggler').click(function (event) {
            $('#scale_help').toggle();
            $('#scale_help_icons').toggle();
        });

        $('#scale_hider').click(function (event) {
            var cont = $('#scale_container');
            if (cont.is(':visible')) {
               cont.hide();
               $('#scale_toggler').hide();
               $(this).text("show stats");
            } else {
               cont.show();
               $('#scale_toggler').show();
               $(this).text("hide stats");
            }
        });
    });

    window.onresize = function (event) {
        bop.resizeDiv();
    };

    bop.resizeDiv =  function () {
        bop.x_full = $(window).width();
        bop.y_full = $(window).height();
        $('#all').css({'height': bop.y_full + 'px'});
        $('#map-container').css({'height':  bop.y_full + 'px'});
        bop.adjust_result_panel_container_height();
    };

    bop.adjust_result_panel_container_height = function () {
        $('#result_panel_container').css({
            'height': bop.y_full - ($('#query_panel').height() + 20) + 'px',
            'overflow': 'auto'
        });
    };
});
