function carousel_size() {
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

$(window).on("load", function(e) {
    var windowWidth = $(window).width();
    var windowHeight = $(window).height();

    carousel_size();

    $(window).on("resize", function(e) {
        carousel_size();
    });
});

