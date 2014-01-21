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
        $('#result_panel_container').css({'height': bop.y_full - $('query_panel').height() + 'px',
                                          'overflow': 'scroll'});
    };
});
