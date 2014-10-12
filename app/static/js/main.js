$('[data-toggle=collapse]').click(function(){
  var attr = $(this).attr("data-target");
  $('a.collapsible[data-toggle=collapse]').each(function(){
    var new_attr = $(this).attr("data-target");
    if ( $(new_attr).hasClass("in")  && new_attr != attr ) {
      $(new_attr).removeClass("in");
      $(new_attr).fadeOut();
    } else if ( $(attr).hasClass("in") ) {
      $(attr).fadeOut();
    } else {
      $(attr).fadeIn();
    }
  });
});

$('#confirm-delete').on('show.bs.modal', function(e) {
  $(this).find('.danger').attr('href', $(e.relatedTarget).data('href'));
  $('.debug-url').html('Þú ert við það að fara að eyða færslu með titilinn: <strong>' + $(e.relatedTarget).data('title') + '</strong> <br> Ertu viss?');
});

$('#content_left, #admin_left').affix({
  offset: {
    top: function() {
      if ( $('#content_left, #admin_left').outerHeight(true) >= $(window).height() ) {
        return 310 - ($(window).height() - $('#content_left, #admin_left').outerHeight(true));
      }
      return $('#content_left, #admin_left').attr('data-affix-top');
    },
    bottom: 100
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
