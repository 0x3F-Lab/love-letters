// ----------   USER PROFILE ----------

$(document).ready(function () {
  $("#editButton").click(function () {
    $("#editForm").toggle();
  });

  $("#changePasswordButton").click(function () {
    $("#passwordForm").toggle();
  });
});

// document.getElementById('password1').addEventListener('input', function() {
//   var password = this.value;
//   var errorMessage = 'Password must:';

//   if (password.length < 8) {
//       errorMessage += 'Be at least 8 characters long. ';
//   }
//   if (!/[A-Z]/.test(password)) {
//       errorMessage += 'Contain at least one uppercase letter. ';
//   }
//   if (!/[a-z]/.test(password)) {
//       errorMessage += 'Contain at least one lowercase letter. ';
//   }
//   if (!/[0-9]/.test(password)) {
//       errorMessage += 'Contain at least one digit. ';
//   }
//   if (!/[\!\@\#\$\%\^\&\*\(\)\_\+]/.test(password)) {
//       errorMessage += 'Contain at least one special character (e.g., !@#$%^&*). ';
//   }

//   this.setCustomValidity(errorMessage);
//   // Update the validity state immediately if using Bootstrap to reflect visual feedback
//   this.reportValidity();
// });




$(document).ready(function() {
  $('#signUpForm').submit(function(e) {
      e.preventDefault(); // Prevent the default form submission

      // Serialize the form data.
      var formData = $(this).serialize();

      $.ajax({
          type: "POST",
          url: $(this).attr('action'),
          data: formData,
          dataType: 'json',
          success: function(response) {
              $('#errorMessages').empty(); // Clear previous errors

              if (response.status === 'success') {
                  var redirectUrl = $('#signUpForm').data('redirect-url');
                  window.location.href = redirectUrl; // redirect to home page
              } else if (response.status === 'error') {
                  // Display error messages
                  $('#errorMessages').text(response.message); // Display error message
              }
          }
      });
  });
});

