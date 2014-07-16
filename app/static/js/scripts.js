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

$(function() {
  $(".fb-login-button").click(function() {
    console.log("Clicked");
    FB.login(function(response) {
      if (response.authResponse) {
        console.log("Welcome! Fetching your information...");
        $.cookie("user_id", response.authResponse.userID);
        $.cookie("access_token", response.authResponse.accessToken);
        window.location = "#{oauth_facebook_callback_url}";
      } else {
        console.log("User cancelled login or did not fully authorize.");
      }
    }, {scope: 'publish_stream,offline_access,email,user_events,create_event,user_location'});
  });
});
