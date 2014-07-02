$('#content_left').affix({
  offset: {
    top: 310,
    bottom: function() {
      return (this.bottom = $('footer').outerHeight(true))
    }
  }
});	

$('#admin_left').affix({
  offset: {
    top: 0,
    bottom: function() {
      return (this.bottom = $('footer').outerHeight(true))
    }
  }
});	


$(document).ready(function() {
  var windowHeight   = $(window).height();
  var documentHeight = $(document).height();
  var footerHeight   = $('.footer').height();
  var footerTop      = $('.footer').position().top + footerHeight;

  if ( footerTop < windowHeight ) {
    $('.footer').css('margin-top', (windowHeight - footerTop) + 'px');
  } else if ( documentHeight > windowHeight && $('#admin_left').length ) {
    $('.footer').css('margin-top', 60 + (documentHeight - footerTop) + 'px');
  }

  var img_width = $('div.img-resize').width();
  $('img.img-resize').width(img_width);

  $(window).resize(function() {
    var img_width = $('div.img-resize').width();
    $('img.img-resize').width(img_width);
  });
});
