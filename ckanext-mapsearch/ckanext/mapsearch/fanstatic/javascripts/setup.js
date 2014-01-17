this.ckan.module('mapsearch-setup', function ($, _) {
    if (typeof bop === 'undefined') {bop = {}}

    $(document).ready(function () {
        bop.resizeDiv();
        $('#keyword_search_input').autocomplete({
           delay: 500,
           source: function(current, display_response) {
               bop.request_completion(display_response)
           },
           minLength: 3,
        })
        $('#keyword_search_input').keypress(function( event ) {
          if ( event.which == 13 ) {
            event.preventDefault();
          }})
        $('#keyword_clear_button').click(function( event ) {
            $('#keyword_search_input').val("");
        })
    });

    bop.request_data = function () {
        bop._do_request('/mapsearch/query_datasets');
    }

    bop.request_completion = function (success_handler) {
        bop._do_request('/mapsearch/text_complete', success_handler);
    }

    bop._do_request = function (path, success_handler) {
        // TODO: cover AJAX-error case
        var q = $('#keyword_search_input').val();
        var bound_string = $('#ext_bbox').val();
        success_handler = success_handler || bop.display_search_results

        $.get(path + '?q=' + q + '&bbox=' + bound_string,
            function (response) {
                success_handler(JSON.parse(response));
            }
        );
    };

    bop.display_search_results = function (results) {
        var container = $('#result_panel_container');
        container.empty();
        $.each(results, function (idx, result) {
            var panel = bop.make_result_panel(result)
            bop.insert_result_panel(panel);
        })
        bop.update_result_list_presentation_mode();
        // TODO: take out global
        a = results[0]
    }

    window.onresize = function (event) {
        bop.resizeDiv();
    }

    bop.resizeDiv =  function () {
        bop.x_full = $(window).width();
        bop.y_full = $(window).height();
        $('#all').css({'height': bop.y_full + 'px'});
        $('#map-container').css({'height':  bop.y_full + 'px'});
    }
})
