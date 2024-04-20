// ----------   USER PROFILE ----------

$(document).ready(function () {
  $("#editButton").click(function () {
    $("#editForm").toggle();
  });

  $("#changePasswordButton").click(function () {
    $("#passwordForm").toggle();
  });
});

// Sign-up Form validation

$(document).ready(function() {
  $('#signUpForm').submit(function(e) {
      e.preventDefault();  // Prevent the default form submission
      var formData = $(this).serialize();  // Serialize the form data

      $.ajax({
          type: "POST",
          url: $(this).attr('action'),
          data: formData,
          dataType: 'json',
          success: function(response) {
              // Handle the success scenario (200)
              var redirectUrl = $('#signUpForm').data('redirect-url');
              window.location.href = redirectUrl; // Redirect to home page
          },
          error: function(xhr, status, error) {
              // Handle the error scenario
              $('.error-message').remove();  // Clear previous error messages

              // Parse the JSON error message from the server
              var response = JSON.parse(xhr.responseText);
              if (response.status === 'error') {
                  for (var fieldName in response.message) {
                      var message = response.message[fieldName];
                      var $inputField = $('#' + fieldName);
                      $inputField.after('<div class="error-message" style="color:red;">' + message + '</div>');
                  }
              } else {
                  console.log("Error: " + xhr.status + " - " + error);
              }
          }
      });
  });
});


// Basic client side validation
// Bootstrap 'required' field handles empty fields



