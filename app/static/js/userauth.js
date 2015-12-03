/**
 * Created by Han on 12/2/15.
 */
$(function () {
    var email;
    $('#email_field').on('change', function() {
        var temp = $('#email_field').val()
        if (temp !== undefined) {
            email = temp;
        }
        console.log(email)
    });
    $('#login-button').bind('click', function(event) {
        event.preventDefault();
        var data = {
            email : email
        };
        $.getJSON($SCRIPT_ROOT + '/logged_in', data, function() {
            console.log("submitted");
        })
    });

    $('#submit_dietary').bind('click', function(event) {
        event.preventDefault();
        var dietary = 0;
        if ($('#vegetarian').hasClass("active")) {dietary += 1024;}
        if ($('#vegan').hasClass("active")) {dietary += 512;}
        if ($('#gluten_free').hasClass("active")) {dietary += 256;}
        if ($('#eggs').hasClass("active")) {dietary += 128;}
        if ($('#milk').hasClass("active")) {dietary += 64;}
        if ($('#peanuts').hasClass("active")) {dietary += 32;}
        if ($('#treenuts').hasClass("active")) {dietary += 16;}
        if ($('#fish').hasClass("active")) {dietary += 8;}
        if ($('#shellfish').hasClass("active")) {dietary += 4;}
        if ($('#wheat').hasClass("active")) {dietary += 2;}
        if ($('#soy').hasClass("active")) {dietary += 1;}
        var data = {
            name : $('#name_field').val(),
            dietary : dietary
        }
        $.getJSON($SCRIPT_ROOT + '/submit_dietary', data, function() {
            console.log("submitted");
        })
    });
});