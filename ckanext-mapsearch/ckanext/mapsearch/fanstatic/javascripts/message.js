this.ckan.module('mapsearch-message', function ($, _) {
    if (typeof bop === 'undefined') {bop = {};}
    bop.display_message = function (msg) {
        var cont = $('#mapsearch_flash'),
            ele = $('#message_prototype').clone().show();
        ele.attr('id', Number(new Date()));
        ele.html(msg);
        cont.append(ele);
        setTimeout(function () {
            ele.hide('slow', function () {
                ele.remove();
            });
        }, 3000);
    };
});
