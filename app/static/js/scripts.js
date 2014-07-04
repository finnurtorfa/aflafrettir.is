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

function set_height() {
  boxes = $('.maxheight');
  boxes.css({'height':''});
  maxHeight = Math.max.apply(
    Math, boxes.map(function() {
      return $(this).outerHeight();
    }).get());
  boxes.outerHeight(maxHeight);
}

$(document).ready(function() {
  var windowHeight   = $(window).height();
  var documentHeight = $(document).height();
  var footerHeight   = $('#footer').height();
  var footerTop      = $('#footer').position().top + footerHeight;

  if ( footerTop < windowHeight ) {
    $('#footer').css('margin-top', (windowHeight - footerTop - footerHeight - 20) + 'px');
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

  set_height();

});
