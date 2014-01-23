this.ckan.module('mapsearch-setup', function ($, _) {
    if (typeof bop === 'undefined') {bop = {}};

    $(document).ready(function () {
        bop.resizeDiv();
        bop.highlightStyle = {color: '#22CCCC'};
        bop.defaultStyle = {color: '#2222CC'};
        $('#keyword_search_input').autocomplete({
           delay: 500,
           select: bop.request_datasets,
           source: function(current, display_response) {
               bop.request_completion(display_response);
           },
           minLength: 2,
        });
        $('#keyword_search_input').keypress(function( event ) {
            if (event.which == 13) {
                event.preventDefault();
                bop.request_datasets();
            }});
        $('#keyword_clear_button').click(function( event ) {
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
        $('#result_panel_container').css({'height': bop.y_full - ($('#query_panel').height() + 20) + 'px',
                                          'overflow': 'auto'});
    };
});
