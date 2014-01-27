
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
        bop._do_request('/api/3/action/package_search');
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
          'url': bop.solr_url + '/suggest',
          'data': {'wt':'json', 'q': q},
          'success': function(data) {
                   if (data.spellcheck.suggestions.length > 0) {
                       success_handler(data.spellcheck.suggestions[1].suggestion);
                   }
               },
          'dataType': 'jsonp',
          'jsonp': 'json.wrf'
        });
    };

    bop._do_request = function (path, success_handler, options) {
        // TODO: cover AJAX-error case
        var q = $('#keyword_search_input').val();
        var bound_string = $('#ext_bbox').val();
        success_handler = success_handler || bop.new_search_results;
        var params = '?q=' + q + '&ext_bbox=' + bound_string
        if (options && options.scale) params += '&ext_scale=' + options.scale;
        if (options && typeof options.rows == 'number') {
            params += '&rows=' + options.rows;
        } else {
            params += '&rows=' + bop.dataset_query_limit;
        }
        $.get(path + params,
            function (response) {
                if (!options || !options.scale) {
                    bop.current_results = response.result;
                }
                success_handler(response);
            }
        );
    };
});
