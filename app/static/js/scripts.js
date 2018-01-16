function onResize() {
    carousel_img_w = $('.carousel-inner .carousel-item img').width()
    carousel_img_h = $('.carousel-inner .carousel-item img').height()
    ratio = carousel_img_w / carousel_img_h;

    carousel_width = $('.carousel-inner .carousel-item').width()
    carousel_height = carousel_width / ratio;

    if ( carousel_height < 100 ) {
        carousel_height = 100;
    }

    $('.carousel-inner .carousel-item img').width(carousel_width);
    $('.carousel .carousel-item img').height(carousel_height);
    $('.carousel .carousel-item').height(carousel_height);
    $('.carousel').height(carousel_height);

}

$('.card-block table').each(function(){
    $(this).prepend('<thead></thead>')
    $(this).find('thead').append($(this).find("tr:eq(0)"));
  });

$('.card-block table').addClass('table table-striped table-hover table-sm table-responsive');
$('.card-block table').find('colgroup').remove().end().html();
$('.card-block table thead').css({'font-weight': 'bold'});
$('.card-block table td').css({'text-align': 'left',
                              'font-size': '10pt',
                              'font-family': 'sans-serif'});


$(window).on("load", function(e) {
    var windowWidth = $(window).width();
    var windowHeight = $(window).height();

    onResize();

    $(window).on("resize", function(e) {
        onResize();
    });
});

$('.dropdown-menu a.dropdown-toggle').on('click', function(e) {
    if (!$(this).next().hasClass('show')) {
        $(this).parents('.dropdown-menu').first().find('.show').removeClass("show");
    }

    var $subMenu = $(this).next(".dropdown-menu");
    $subMenu.toggleClass('show');

    $(this).parents('li.nav-item.dropdown.show').on('hidden.bs.dropdown', function(e) {
        $('.dropdown-submenu .show').removeClass("show");
    });

    return false;
});

$('#navbarCollapse').on('shown.bs.collapse', function () {
  $('.drop-main').css({'height': 'auto',
                       'overflow-x': 'hidden',
                       'max-height': $(window).height() - 200,
                       'margin': ''});
})

$('#navbarCollapse').on('hidden.bs.collapse', function () {
  $('.drop-main').css({'height': '',
                       'overflow-x': '',
                       'max-height': '',
                       'margin': '19px'});
})
