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
