$(document).ready(function() {
  $('article table').each(function(){
    $(this).wrap('<div class="scroll-table"></div>')
    $(this).prepend('<thead></thead>')
    $(this).find('thead').append($(this).find("tr:eq(0)"));
  });
  $('article table').addClass('ink-table alternating hover');
  $('article table').find('colgroup').remove().end().html();
  $('article table thead').css({'font-weight': 'bold'});
  $('article table td').css({'text-align': 'left',
                             'font-size': '10pt'});
});

