function set_height() {
  carousel_height = $('.carousel-inner .item.active img').height();
  if ( carousel_height < 100 ) {
    carousel_height = 100;
  }

  $('.carousel .item').height(carousel_height);
  $('.carousel').height(carousel_height);
}

$(document).ready(function() {
  var windowHeight   = $(window).height();
  var documentHeight = $(document).height();
  var footerHeight   = $('#footer').height();
  var footerTop      = $('#footer').position().top + footerHeight;

  if ( footerTop < windowHeight ) {
    $('#footer').css('margin-top', (windowHeight - footerTop - footerHeight) + 'px');
  } 

  var img_width = $('div.img-resize').width();
  $('img.img-resize').width(img_width);

  $(window).resize(function() {
    var img_width = $('div.img-resize').width();
    $('img.img-resize').width(img_width);
  });

  $(window).resize(function() {
    set_height();
  });

  $('.carousel-inner .item.active img').on('load', set_height);

  set_height();

  $('.post-body table').each(function(){
    $(this).prepend('<thead></thead>')
    $(this).find('thead').append($(this).find("tr:eq(0)"));
  });
  $('.post-body table').addClass('table table-striped table-hover table-condensed table-responsive');
  $('.post-body table').find('colgroup').remove().end().html();
  $('.post-body table thead').css({'font-weight': 'bold'});
  $('.post-body table td').css({'text-align': 'left',
                                'font-size': '10pt',
                                'font-family': 'sans-serif'});
});

