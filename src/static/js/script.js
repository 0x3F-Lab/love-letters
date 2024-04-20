// ----------   USER PROFILE ----------

$(document).ready(function () {
  $("#editButton").click(function () {
    $("#editFormDiv").toggle();
  });

  $("#changePasswordButton").click(function () {
    $("#passwordFormDiv").toggle();
  });
});

// Sign-up Form validation

$(document).ready(function() {
  $('#signUpForm').submit(function(e) {
      e.preventDefault(); // Prevent the default form submission
      const formData = $(this).serialize(); // Serialize the form data

      $.ajax({
          type: "POST",
          url: $(this).attr('action'),
          data: formData,
          dataType: 'json',
          success: function(response) {
              const redirectUrl = $('#signUpForm').data('redirect-url');
              window.location.href = redirectUrl; // Redirect to home page
          },
          error: function(xhr, status, error) {
              $('.error-message').remove(); // Clear previous error messages

              if (xhr.status === 500) { // Database update failure
                  console.error("Server Error: " + xhr.responseText);
                  alert("We're experiencing technical difficulties. Please try again later.");
              } else if (xhr.status === 400) {
                  const response = JSON.parse(xhr.responseText);
                  if (response.status === 'error') {
                      for (let fieldName in response.message) {
                          let message = response.message[fieldName];
                          let $inputField = $('#' + fieldName);
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
      const formData = $(this).serialize(); // Serialize the form data

      $.ajax({
          type: "POST",
          url: $(this).attr('action'), 
          data: formData,
          dataType: 'json',
          success: function(response) {
              if (response.status === 'success') {
                  const redirectUrl = $('#signUpForm').data('redirect-url');
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
      const formData = $(this).serialize(); // Serialize the form data

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
              const response = JSON.parse(xhr.responseText);
              console.log(response)
              if (response.status === 'error') {
                  for (let fieldName in response.message) {
                      let message = response.message[fieldName];
                      let $inputField = $('#' + 'edit_' + fieldName);
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



// Changing password validation

$(document).ready(function() {
  $('#passwordForm').submit(function(e) {
      e.preventDefault(); // Prevent the default form submission
      const formData = $(this).serialize(); // Serialize the form data

      $.ajax({
          type: "POST",
          url: $(this).attr('action'),
          data: formData,
          dataType: 'json',
          success: function(response) {
              if (response.status === 'success') {
                  location.reload();
              }
          },
          error: function(xhr) {
              $('.error-message').remove();
              if (xhr.status === 500) {
                  console.error("Server Error: " + xhr.responseText);
                  $('#passwordError').text("We're experiencing technical difficulties. Please try again later.").show();
              } else if (xhr.status === 400) {
                  const response = JSON.parse(xhr.responseText);
                  $('#passwordError').text(xhr.responseJSON.message).show();
              } else {
                  console.error("Error: " + xhr.status + " - " + xhr.statusText);
              }
          }
      });
  });
});