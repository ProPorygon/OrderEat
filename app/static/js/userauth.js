/**
 * Created by Han on 12/2/15.
 */
function onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    var name = profile.getName();
    var id_token = googleUser.getAuthResponse().id_token;
    var user = {
        "id" : id_token,
        "name" : name,
        "dietary" : 0
    }
    $(function() {
        $.getJSON($SCRIPT_ROOT + '/logged_in', user);
    });
}

function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
        $(function() {
            $.getJSON($SCRIPT_ROOT + '/logout');
        });
    });
}