/**
 * Created by Han on 12/2/15.
 */
$(function () {
    $('#login-button').on('click', function(event) {
        event.preventDefault();
        var email = {
            "email" : $('#email_field').val()
        }
        $.getJSON($SCRIPT_ROOT + '/logged_in', email, function() {
            console.log("submitted");
        })
    });

    $('#submit_dietary').on('click', function(event) {
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
            "name" : $('#name_field').val(),
            "dietary" : dietary
        }
        $.getJSON($SCRIPT_ROOT + '/submit_dietary', data, function() {
            console.log("submitted");
        })
    });
});