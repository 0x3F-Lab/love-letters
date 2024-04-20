// ----------   USER PROFILE ----------

$(document).ready(function () {
  $("#editButton").click(function () {
    $("#editDiv").toggle();
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
              var redirectUrl = $('#signUpForm').data('redirect-url');
              window.location.href = redirectUrl; // Redirect to home page
          },
          error: function(xhr, status, error) {
              $('.error-message').remove(); // Clear previous error messages

              if (xhr.status === 500) { // Database update failure
                  console.error("Server Error: " + xhr.responseText);
                  alert("We're experiencing technical difficulties. Please try again later.");
              } else if (xhr.status === 400) {
                  var response = JSON.parse(xhr.responseText);
                  if (response.status === 'error') {
                      for (var fieldName in response.message) {
                          var message = response.message[fieldName];
                          var $inputField = $('#' + fieldName);
                          $inputField.after('<div class="error-message" style="color:red;">' + message + '</div>');
                      }
                  }
              } else {
                  console.log("Error: " + xhr.status + " - " + error);
              }
          }
      });
  });
});

// Log in validation

$(document).ready(function() {
  $('#loginForm').submit(function(e) {
      e.preventDefault(); // Prevent the default form submission
      var formData = $(this).serialize(); // Serialize the form data

      $.ajax({
          type: "POST",
          url: $(this).attr('action'), 
          data: formData,
          dataType: 'json',
          success: function(response) {
              if (response.status === 'success') {
                  var redirectUrl = $('#signUpForm').data('redirect-url');
                  window.location.href = redirectUrl; // Redirect to home page
              }
          },
          error: function(xhr, status, error) {
              if (xhr.status === 401) {
                $('#loginError').text(xhr.responseJSON.message).show(); // Display error message from the server
              } else {
                  console.error("Error: " + xhr.status + " - " + xhr.statusText);
                  $('#loginError').text('An unexpected error occurred. Please try again.').show();
              }
          }
      });
  });
});;

// Update user information validation

$(document).ready(function() {
  $('#editForm').submit(function(e) {
      e.preventDefault(); // Prevent the default form submission
      var formData = $(this).serialize(); // Serialize the form data

      $.ajax({
          type: "POST",
          url: $(this).attr('action'),
          data: formData,
          dataType: 'json',
          success: function(response) {
              if (response.status === 'success') {
                  location.reload(); // Reload the page to reflect changes
              }
          },
          error: function(xhr, status, error) {
            $('.error-message').remove();
            if (xhr.status === 500) { // Database update failure
              console.error("Server Error: " + xhr.responseText);
              alert("We're experiencing technical difficulties. Please try again later.");
            } else if (xhr.status === 400) {
              var response = JSON.parse(xhr.responseText);
              console.log(response)
              if (response.status === 'error') {
                  for (var fieldName in response.message) {
                      console.log("Appending error to:", $inputField);
                      var message = response.message[fieldName];
                      var $inputField = $('#' + 'edit_' + fieldName);
                      $inputField.after('<div class="error-message" style="color:red;">' + message + '</div>');
                  }
              }
            } else {
                console.log("Error: " + xhr.status + " - " + error);
            }
          }
      });
  });
});




