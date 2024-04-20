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
      e.preventDefault(); // Prevent the default form submission
      var formData = $(this).serialize(); // Serialize the form data

      $.ajax({
          type: "POST",
          url: $(this).attr('action'), 
          data: formData,
          dataType: 'json',
          success: function(response) {
              if (response.status === 'error') {
                  // Clear previous error messages
                  $('.error-message').remove();

                  // Display error messages next to the respective form fields
                  for (var fieldName in response.message) {
                      var message = response.message[fieldName];
                      var $inputField = $('#' + fieldName); 
                      $inputField.after('<div class="error-message" style="color:red;">' + message + '</div>');
                  }
              } else if (response.status === 'success') {
                var redirectUrl = $('#signUpForm').data('redirect-url');
                window.location.href = redirectUrl; // redirect to home page
              }
          },
          error: function(xhr, status, error) {
              console.log("Error: " + xhr.status + " - " + error);
          }
      });
  });
});

