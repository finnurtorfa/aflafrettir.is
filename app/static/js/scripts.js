$('#content_left').affix({
  offset: {
    top: 310,
    bottom: function() {
      return (this.bottom = $('footer').outerHeight(true))
    }
  }
});	
