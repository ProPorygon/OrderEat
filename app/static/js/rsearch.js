$('#searchbar').on('input',function(e){
    var searchtext = $(this)[0].value.toLowerCase()
    $('.list-group .list-group-item').each(function () {
        var menuitem = $(this)[0].innerText.toLowerCase();
        if (menuitem.indexOf(searchtext) == -1) {
            $(this).fadeOut();
        } else {
            $(this).fadeIn();
        }
    });
});