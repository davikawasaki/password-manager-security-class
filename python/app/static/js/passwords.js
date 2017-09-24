$(document).ready(function(){
    // the "href" attribute of the modal trigger must specify the modal ID that wants to be triggered
    $('.modal').modal();
});

// Hides recovery master password code
$('#reccode-list-passwords').on('click', function() {
    $('#recoveryPasswordRegisterModal').addClass('display-none');
});

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

// Adds passwordConfirm validation function
$('#addPassword').on('focusout', function () {
    if ($(this).val() != $('#addPasswordConfirm').val()) {
        $('#addPasswordConfirm').removeClass('valid').addClass('invalid');
    } else {
        $('#addPasswordConfirm').removeClass('invalid').addClass('valid');
    }
});
// Adds passwordConfirm validation function
$('#addPasswordConfirm').on('keyup', function () {
    if ($(this).val() != $('#addPassword').val()) {
        $(this).removeClass('valid').addClass('invalid');
    } else {
        $(this).removeClass('invalid').addClass('valid');
    }
});

// Dismiss modals
$('#cancelEditModalBtn').on('click', function() {
    $('#editModal').modal('close');
});
$('#cancelDeleteModalBtn').on('click', function() {
    $('#deleteModal').modal('close');
});
$('#cancelAddModalBtn').on('click', function() {
    $('#addModal').modal('close');
});

// Get row information to remove data
$(".delete-data-row").on('click', function() {
    var $row = $(this).parent().parent();    // Find the row
    // Set delete text
    $('#removeInfoName').val($row.find(".data-name").text());
    $('#removeLogin').val($row.find(".data-login").text());
    $('#removePassword').val($row.find(".data-password").text());
    $('#removeTimestamp').val($row.find(".data-timestamp").text());
});

// Get row information to update data
$(".edit-data-row").on('click', function() {
    var $row = $(this).parent().parent();    // Find the row
    // Set delete text
    $('#updateInfoName').val($row.find(".data-name").text());
    $('#updateLogin').val($row.find(".data-login").text());
    $('#updatePassword').val($row.find(".data-password").text());
    $('#updateTimestamp').val($row.find(".data-timestamp").text());
});