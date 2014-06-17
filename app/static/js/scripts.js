$('#content_left').affix({
      offset: {
        top: 510,
        bottom: function() {
          return (this.bottom = $('footer').outerHeight(true))
        }
      }
});	
$('#content_right').affix({
      offset: {
        top: 510,
        bottom: function() {
          return (this.bottom = $('footer').outerHeight(true));
        }
      }
});	
