/* global bop */

this.ckan.module('mapsearch-transport', function ($, _) {
    bop.request_datasets = function () {
        bop._do_request('/mapsearch/query_datasets');
    };

    bop.request_completion = function (success_handler) {
        var q = $('#keyword_search_input').val();
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

    bop._do_request = function (path, success_handler) {
        // TODO: cover AJAX-error case
        var q = $('#keyword_search_input').val();
        var bound_string = $('#ext_bbox').val();
        success_handler = success_handler || bop.display_search_results;

        $.get(path + '?q=' + q + '&bbox=' + bound_string + '&rows=' + bop.dataset_query_limit,
            function (response) {
                success_handler(JSON.parse(response));
            }
        );
    };
});
