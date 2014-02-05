
var bop;

this.ckan.module('mapsearch-transport', function ($, _) {
    var scale_row_dict = {small: false, too_small:0, big:false, too_big:0};
    bop.request_datasets_for_scale = function (scale) {
         bop._do_request('/api/3/action/package_search',
                          function(response) {
                              var container  = $('.omitted_' + scale);
                              container.find('span').text(response.result.count);
                              if (response.result.count < 1) {
                                container.find('a').hide()
                              } else {
                                container.find('a').show()
                              }
                              bop.omitted_results[scale] = response.result;
                          },
                          {scale: scale, rows: scale_row_dict[scale]});
    }

    bop.request_datasets = function () {
        bop._do_request('/api/3/action/package_search', bop.new_search_results, {scale: 'normal'});
        bop.request_datasets_for_scale('too_small');
        bop.request_datasets_for_scale('small');
        bop.request_datasets_for_scale('big');
        bop.request_datasets_for_scale('too_big');
    };

    bop.request_completion = function (success_handler) {
        var q = $('#keyword_search_input').val();
        /* TODO: make handling more intelligent
         * split and reassemble to-be-completed word
         * */
        if (q.match(/.+:.+/)) {return;}
        $.ajax({
          'url': '/mapsearch/textcomplete',
          'data': {'q': q},
          'success': function(data) {
                  success_handler(data);
               },
          'dataType': 'json',
        });
        return
    };

    var setupSpinner = function (scale) {
        var spinner = $('#search_spinner_prototype').clone();
        spinner.attr('id', 'search_spinner_' + scale);
        spinner.show();
        var cont = (scale == 'normal' ? $('.normal_scale_count') : $('.omitted_' + scale)).find("span")
        cont.html(spinner)
        return spinner.show();
    };

    bop._do_request = function (path, success_handler, options) {
        var q = $('#keyword_search_input').val(),
            bound_string = $('#ext_bbox').val(),
            params = '?q=' + q + '&ext_bbox=' + bound_string,
            spinner = setupSpinner(options.scale).show();
        if (options && options.scale) params += '&ext_scale=' + options.scale;
        if (options && typeof options.rows == 'number') {
            params += '&rows=' + options.rows;
        } else {
            params += '&rows=' + bop.dataset_query_limit;
        }
        $.get(path + params,
            function (response) {
                if (options.scale == 'normal') {
                    bop.current_results = response.result;
                }
                success_handler(response);
            })
        .always(function (e) {
                    bop.reset_gui_after_load(spinner);
                })
        .fail(function (e) {bop.display_message("search failed<br/>" + e)});
    };
    bop.reset_gui_after_load = function (spinner) {
        spinner && spinner.hide();
        $('.displayed').removeClass('displayed');
        bop.small_extents_are_displayed = false;
    };
});
