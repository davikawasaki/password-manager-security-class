// Adds passwordConfirm validation function
$('#password').on('focusout', function () {
    if ($(this).val() != $('#passwordConfirm').val()) {
        $('#passwordConfirm').removeClass('valid').addClass('invalid');
    } else {
        $('#passwordConfirm').removeClass('invalid').addClass('valid');
    }
});
// Adds passwordConfirm validation function
$('#passwordConfirm').on('keyup', function () {
    if ($(this).val() != $('#password').val()) {
        $(this).removeClass('valid').addClass('invalid');
    } else {
        $(this).removeClass('invalid').addClass('valid');
    }
});
