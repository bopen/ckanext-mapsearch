/* global bop:true */
var bop;

this.ckan.module('mapsearch-result_navigation', function ($, _) {
    // this is called when the page loads
    bop.result_nav.setup = function () {
        $('.navigation_arrow').click(function () {
            var dir = ($(this).data('dir'));
            if (dir === 'next' && bop.result_nav.current_page < bop.result_nav.num_of_pages - 1) {
                bop.result_nav.current_page++;
            } else if (dir === 'previous' && bop.result_nav.current_page > 0) {
                bop.result_nav.current_page--;
            } else {
                return;
            }
            bop.result_nav.update_ui();
            bop.display_search_results({keep_small: true});
        });

        $('.navigation_number').click(function () {
            bop.result_nav.current_page = Number($(this).data('idx')) - 1;
            bop.result_nav.update_ui();
            bop.display_search_results({keep_small: true});
        });
    };

    bop.result_nav.update_ui = function () {
        var current_result_start_idx = bop.result_nav.current_page * bop.results_per_page + 1,
            total = bop.current_results.count,
            current_result_end_idx = Math.min(current_result_start_idx +
                                                 bop.results_per_page - 1,
                                              total)
        $('.navigation_number').removeClass('selected');
        $('#nav_' + (bop.result_nav.current_page + 1)).addClass('selected');

        if (bop.current_results.results.length == 0) {
          $('#pagination_range_display').hide()
        } else {
          $('#pagination_range_display').show()
          $('#current_range_display').text(String(current_result_start_idx) + " - " +
                                         current_result_end_idx);
        }
    };

    // this method should be called when new results arrive from the server
    bop.result_nav.update = function () {
        var results = bop.current_results.results;
        bop.result_nav.current_page = 0;
        bop.result_nav.num_of_pages = Math.ceil(
            Math.min(bop.current_results.count, bop.max_result_display) / bop.results_per_page);
        $('#current_total_display').text(results.length <= bop.max_result_display ? results.length : String(bop.max_result_display) + "+");
        $('#navigation_links').hide();
        $('.navigation_number').hide();
        if (results.length > bop.results_per_page) {
            $('#navigation_links').show();
            $('.navigation_number').each(function(idx, ele) {
                 if (Number($(ele).data('idx')) <= bop.result_nav.num_of_pages){
                     $(ele).show();
                 }
            });
        }
        bop.result_nav.update_ui();
    };
});
