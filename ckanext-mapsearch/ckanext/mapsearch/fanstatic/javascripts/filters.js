var bop, _;

this.ckan.module('mapsearch-filters', function ($, _) {
    bop.setup_filter_panel = function () {
        $('#filter_toggler').click(function () {
            $('#filter_panel').toggle();
            bop.adjust_result_panel_container_height();
        });
        $('#filter_panel').on('click', '.filter_toggle', function () {
            var ele = $(this),
                filter = ele.data('filter'),
                input = $('#keyword_search_input'),
                current_q = input.val();
            if (bop.filters.indexOf(filter) !== -1) {
                bop.filters.splice(bop.filters.indexOf(filter), 1);
                ele.removeClass('on');
                input.val(current_q.replace(new RegExp(" ?" + filter + " ?"), ""));
            } else {
                bop.filters.push(filter);
                input.val(current_q + " " + filter);
                ele.addClass('on');
            }
            bop.request_datasets();
        });
    };
    bop.update_filter_panel = function () {
        var tags = {},
            formats = {};
        $.each(bop.current_results, function (idx, result) {
             if (result.tags.length > 0) {
                 $.each(result.tags, function (iidx, tag) {
                     if (tags[tag.display_name]) {tags[tag.display_name]++;}
                     else {tags[tag.display_name] = 1;}
                 });
             }
             if (result.resources.length > 0) {
                 $.each(result.resources, function (iidx, resource) {
                     if (formats[resource.format]) {
                         formats[resource.format]++;
                     } else {
                         formats[resource.format] = 1;
                     }
                 });
             }
        });
        var num_sort = function(a,b) {return a[0] - b[0];};
        tags = $.map(tags, function (value, key) {return [[value, key]];}).sort(num_sort).reverse();
        formats = $.map(formats, function (value, key) {return [[value, key]];}).sort(num_sort).reverse();
        var tag_container = $('#tags_filter_container');
        tag_container.empty();
        var format_container = $('#formats_filter_container');
        format_container.empty();
        create_links(tags, "tags", tag_container);
        create_links(formats, "res_format", format_container);
    };
    var create_links = function (items, filter_name, container) {
        $.each(items.slice(0, bop.num_filters_to_display), function (idx, item) {
            if (item[1] === '') {return;}
            var link = $('#filter_toggle_proto').clone(),
                filter_string = filter_name + ":" + item[1];
            link.show().text(item[1].replace(/-/g, "‑") + "\xA0(" + item[0] + ") ");
            link.data('filter', filter_string);
            if (bop.filters.indexOf(filter_string) >= 0) {link.addClass('on');}
            container.append(link);
        });
    };
});
