$(document).ready(function () {
    $('[data-toggle=offcanvas]').click(function () {
        $('.row-offcanvas').toggleClass('active');
        $('.showhide').toggle();
    });
});

function subscribe() {
    if (validateEmail($('#emailTextbox').val())) {
        $('#emailButton').prop("disabled", true);
        registerEmail($('#emailTextbox').val());
    } else {
        $('#emailText').css("color", "red");
        $('#emailText').html("Invalid email address");
    }
}

function subscribexs() {
    if (validateEmail($('#emailTextbox-xs').val())) {
        $('#emailButton-xs').prop("disabled", true);
        registerEmail($('#emailTextbox-xs').val());
    }
}

function registerEmail(emailAddress) {
    $.ajax({
        url: "/ajax/addEmail.php?email=" + emailAddress, success: function (result) {
            if (result == "Inserted") {
                $('#emailText').css("color", "black");
                $('#emailText').html("Thank you for subscribing!");

                $('#emailInputs-xs').hide();
                $('#emailStatus-xs').html("Thank you for subscribing!");
                $('#emailStatus-xs').fadeIn();

            } else if (result == "Duplicate") {
                $('#emailText').css("color", "red");
                $('#emailText').html("You are already subscribed");

                $('#emailInputs-xs').hide();
                $('#emailStatus-xs').html("You have already subscribed");
                $('#emailStatus-xs').fadeIn();

            } else {
                $('#emailText').css("color", "red");
                $('#emailText').html("Oops! Please try again later");

                $('#emailInputs-xs').hide();
                $('#emailStatus-xs').html("Oops! Please try again later");
                $('#emailStatus-xs').fadeIn();
            }
            $('#emailButton').prop("disabled", false);
            $('#emailButton-xs').prop("disabled", false);
        }
    });
}

function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}