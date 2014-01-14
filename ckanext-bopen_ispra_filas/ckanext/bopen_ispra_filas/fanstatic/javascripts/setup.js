bop = {};

$(document).ready(function () {
    bop.resizeDiv();
});

window.onresize = function (event) {
    bop.resizeDiv();
}

bop.resizeDiv =  function () {
    bop.x_full = $(window).width();
    bop.y_full = $(window).height();
    $('#all').css({'height': bop.y_full + 'px'});
    $('#map-container').css({'height':  bop.y_full + 'px'});
}
