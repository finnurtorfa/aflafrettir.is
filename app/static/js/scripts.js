function carousel_size() {
  carousel_width = $('.carousel-inner .item').width()
  $('.carousel-inner .item.active img').width(carousel_width);
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
    carousel_size();
  });

  $('.dropdown').mouseenter(function() {
    $(this).addClass('open');
  });

  $('.dropdown').mouseleave(function() {
    $(this).removeClass('open');
  });

  $('.carousel-inner .item.active img').on('load', carousel_size);

  carousel_size();

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

  $('#content_left, #admin_left').affix({
    offset: {
      top: function() {
        if ( $('#content_left, #admin_left').outerHeight(true) >= $(window).height() ) {
          return 310 - ($(window).height() - $('#content_left, #admin_left').outerHeight(true));
        }
        return $('#content_left, #admin_left').attr('data-affix-top');
      },
      bottom: 300
    }
  });
  
  $('#content_left, #admin_left').on('affixed.bs.affix', function() {
    if ( $(this).outerHeight(true) >= $(window).height() ) {
      $(this).css('top', ($(window).height() - $(this).outerHeight(true)) + 'px');
    } else {
      $(this).css('top', '67px');
    }
  });
  
  $('#content_left, #admin_left').on('affixed-top.bs.affix', function() {
    $(this).css('top', '0px');
  });
});

