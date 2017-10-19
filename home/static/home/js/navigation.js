$('ul.filter-portfolio')
    .find('li:gt(5)')
    .hide()
    .end()
    .append(
    $('<li><a href="#">Show More Tags</a></li>').click( function(){
        $(this).siblings(':hidden').show().end().remove();
    })
);