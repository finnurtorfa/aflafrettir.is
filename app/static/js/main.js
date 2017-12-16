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
  //<![CDATA[
jQuery.cookie = function (key, value, options) {
    // key and at least value given, set cookie...
    if (arguments.length > 1 && String(value) !== "[object Object]") {
        options = jQuery.extend({}, options);

        if (value === null || value === undefined) {
            options.expires = -1;
        }

        if (typeof options.expires === 'number') {
            var days = options.expires, t = options.expires = new Date();
            t.setDate(t.getDate() + days);
        }
        value = String(value);
        return (document.cookie = [
            encodeURIComponent(key), '=',
            options.raw ? value : encodeURIComponent(value),
            options.expires ? '; expires=' + options.expires.toUTCString() : '', // use expires attribute, max-age is not supported by IE
            options.path ? '; path=' + options.path : '',
            options.domain ? '; domain=' + options.domain : '',
            options.secure ? '; secure' : ''
        ].join(''));
    }
    // key and possibly options given, get cookie...
    options = value || {};
    var result, decode = options.raw ? function (s) { return s; } :
    decodeURIComponent;
    return (result = new RegExp('(?:^|; )' + encodeURIComponent(key) +
    '=([^;]*)').exec(document.cookie)) ? decode(result[1]) : null;
};
//]]>

$('.dropdown-menu a.dropdown-toggle').on('click', function(e) {
    if (!$(this).next().hasClass('show')) {
        $(this).parents('.dropdown-menu').first().find('.show').removeClass("show");
    }

    var $subMenu = $(this).next(".dropdown-menu");
    $subMenu.toggleClass('show');

    $(this).parents('li.nav-item.dropdown.show').on('hidden.bs.dropdown', function(e) {
        $('.dropdown-submenu .show').removeClass("show");
    });

    return false;
});
