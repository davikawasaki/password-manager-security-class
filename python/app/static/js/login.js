$(document).ready(function(){
    // the "href" attribute of the modal trigger must specify the modal ID that wants to be triggered
    $('.modal').modal();
});

// Makes Password Confirmation field and Warning Text Fades
function fades(){
  if ($(".warningText").is(":visible")) {
      $(".warningText").animate(
          {
              opacity: "0"
          },
          600,
          function(){
              $(".warningText").slideUp();
          }
      );
  }
  else {
      $(".warningText").slideDown(600, function(){
          $(".warningText").animate(
              {
                  opacity: "1"
              },
              600
          );
      });
  }
  if ($(".passCheck").is(":visible")) {
      $(".passCheck").animate(
          {
              opacity: "0"
          },
          600,
          function(){
              $(".passCheck").slideUp();
          }
      );
  }
  else {
      $(".passCheck").slideDown(600, function(){
          $(".passCheck").animate(
              {
                  opacity: "1"
              },
              600
          );
      });
  }
}

// Changes view from login to register
$('#registerBtn').on('click', function(event) {
  // If user is on Login view
  if(document.getElementById('registerBtn').innerHTML != "Register"){
    // FadesOut warningText and Password Confirmation
    fades();
    // Changes Page Title
    document.getElementById('logo').innerHTML = "Login";
    // Changes SubmitButton Text
    document.getElementById('sendBtn').innerHTML = "<i class='material-icons right'>send</i>Login";
    // Changes RegisterButton Text
    document.getElementById('registerBtn').innerHTML = "Register";
  }
  // If user is on Register view
  else {
    // Changes Page Title
    document.getElementById('logo').innerHTML = "Register";
    // Changes SubmitButton Text
    document.getElementById('sendBtn').innerHTML = "<i class='material-icons right'>send</i>Register";
    // Changes RegisterButton Text
    document.getElementById('registerBtn').innerHTML = "Login";
    // FadesIn warningText and Password Confirmation
    fades();
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
  }
});

$('#sendBtn').on('click', function() {
  console.log(document.getElementById("username").value);
  console.log(document.getElementById("password").value);

  // Change this to resgister function.
  $('#registerModal').modal('open');
});

// Dismiss modals
$('#agreeModalBtn').on('click', function() {
    $('#registerModal').modal('close');
});
