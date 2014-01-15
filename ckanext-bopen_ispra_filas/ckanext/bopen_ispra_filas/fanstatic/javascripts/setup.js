bop = {};

$(document).ready(function () {
    bop.resizeDiv();
    $('#keyword_search_input').autocomplete({
       delay: 500,
       source: function(current, display_response) {
           bop.request_data({q: current.term}, display_response)
       },
       minLength: 3,
    })
});

bop.request_data = function (params, display_response) {
    var q = $('#keyword_search_input').val();

    $.get('/map-search/text_complete?q=' + params.q + '&bbox=' + bop.map.getBounds().toBBoxString(),
           function (r) {
               display_response(JSON.parse(r))
           })
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
