/* global bop */
this.ckan.module('mapsearch-result-panel', function ($, _) {
    /*
     *author: ""
     author_email: ""
     extras: Array[1]
     groups: Array[0]
     id: "9e34aa70-af7e-437c-ac2e-1d38a9489b15"
     isopen: true
     license_id: "cc-by-sa"
     license_title: "Creative Commons Attribution Share-Alike"
     license_url: "http://www.opendefinition.org/licenses/cc-by-sa"
     maintainer: ""
     maintainer_email: ""
     metadata_created: "2014-01-13T12:04:57.261053"
     metadata_modified: "2014-01-14T13:39:07.130159"
     name: "heiderhof"
     notes: "in stuttgart auf der hasenheide"
     num_resources: 1
     num_tags: 3
     organization: Object
     owner_org: "b7cf2b95-94d4-43f0-bf6a-67cbbf451504"
     private: false
     relationships_as_object: Array[0]
     relationships_as_subject: Array[0]
     resources: Array[1]
     revision_id: "0a9fceb2-e7d4-4deb-826f-9b8daaa7f155"
     revision_timestamp: "2014-01-14T11:50:53.688686"
     state: "active"
     tags: Array[3]
     title: "heiderhof"
     tracking_summary: Object
     type: "dataset"
     url: null
     version: null
     */
    if (typeof bop === 'undefined') {bop = {}}

    bop.make_result_panel = function (result, options) {
        var list_item_proto;
        panel = $('#result_panel_prototype').clone();
        panel.attr('id', result.id);
        var title_link = panel.find('.title_link');
        title_link.text(result.title);
        var dataset_url = "/dataset/" + result.id;
        title_link.attr('href', dataset_url);
        title_link.attr('title', "go to detail page");
        panel.find('.notes').html(truncate_notes(result.notes, dataset_url));
        panel.find('.license').text(result.license_title);
        if (result.tags && result.tags.length > 0) {
            var tag_list_container = panel.find('.result_tag_list');
            list_item_proto = tag_list_container.find('.list_item').clone();
            tag_list_container.empty();
            $.each(result.tags, function(idx, tag) {
                var list_item = list_item_proto.clone(),
                    filter_string = "tags:" + tag.display_name;
                list_item.find('a').data('filter', filter_string).text(tag.display_name);
                tag_list_container.append(list_item);
                if (bop.filters.indexOf(filter_string) !== -1) {
                    list_item.find('a').addClass('on');
                }
            });
        } else {
            panel.find('.result_tag_list').remove();
        }
        if (result.groups && result.groups.length > 0) {
            //TODO: implement groups
            panel.find('.groups_container').remove();
            console.log("NotImplementedError: groups present but not shown");
        } else {
            panel.find('.groups_container').remove();
        }
        if (result.resources && result.resources.length > 0) {
            var resources_list_container = panel.find('.result_resources_list');
            list_item_proto = resources_list_container.find('.list_item').clone();
            resources_list_container.empty();
            $.each(result.resources, function(idx, resource) {
                var list_item = list_item_proto.clone();
                list_item.find('a').attr('href', resource.url).text(resource.name || "unnamed file");
                resources_list_container.append(list_item);
            });
        } else {
            panel.find('.result_resources_list').remove();
        }
        if (result.organization) {
            panel.find('.organization').text(result.organization.name);
        } else {
            panel.find('.organization_container').remove();
        }
        panel.find('.created_at').text(new Date(result.metadata_created).toDateString());
        panel.find('.modified_at').text(new Date(result.metadata_modified).toDateString());
        panel.show();
        return panel;
    };

    var truncate_notes = function (notes, url) {
        var limit = 80,
            split = notes.split(" ");
        if (split.length <= limit) {
            return split.join(" ");
        } else {
            var base = split.slice(0, limit).join(" ");
            return base + " ... <a class='descreet_help' href='" + url +
                          "' target='_blank'>(see full notes here)</a>";
        }
    };

    bop.insert_result_panel = function (panel) {
        container = $('#result_panel_container');
        container.append(panel);
    };

    bop.unselect_all_results = function () {
        $('.dataset_result_panel').removeClass("selected");
        bop.result_layer.eachLayer(function(layer){
            try {
                var props = layer.feature.properties;
                if (!props.mapsearch || props.mapsearch != 'small') {
                    layer.setStyle(bop.result_style);
                }
            } catch(err) {}
        });
        bop.update_result_list_presentation_mode();
    }
    bop.select_result = function (elem) {
        var id;
        if (typeof elem == 'string') { 
            id = elem;
            elem = $('#' + elem);
        } else {
            id = elem.attr('id');
        }
        bop.unselect_all_results()
        elem.addClass("selected");
        elem.get(0).scrollIntoView();
        bop.result_layer.eachLayer(
            function (lay) {
              if (lay.feature.properties.id == id) {
                 lay.setStyle(bop.highlightStyle);
              }
            }
        );
        bop.update_result_list_presentation_mode();
    };

    $('#result_panel_container').on('click', ".dataset_result_panel", function (e) {
        if (e.target.tagName != 'A') {
            if ($(e.target).parents('.dataset_result_panel.selected').length == 0) {
                bop.select_result($(this));
                e.preventDefault();
            } else {
                bop.unselect_all_results();
            }
        }
        ev = e;
    });

    bop.update_result_list_presentation_mode = function () {
        $('.dataset_result_panel').find(".hide_when_small").hide();
        $('.dataset_result_panel.selected').find(".hide_when_small").show();
    };
});
