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

$(document).ready(function () {
  $("#signUpForm").submit(function (e) {
    e.preventDefault(); // Prevent the default form submission
    const formData = $(this).serialize(); // Serialize the form data

    $.ajax({
      type: "POST",
      url: $(this).attr("action"),
      data: formData,
      dataType: "json",
      success: function (response) {
        const redirectUrl = $("#signUpForm").data("redirect-url");
        window.location.href = redirectUrl; // Redirect to home page
      },
      error: function (xhr, status, error) {
        $(".error-message").remove(); // Clear previous error messages

        if (xhr.status === 500) {
          // Database update failure
          console.error("Server Error: " + xhr.responseText);
          alert(
            "We're experiencing technical difficulties. Please try again later.",
          );
        } else if (xhr.status === 400) {
          const response = JSON.parse(xhr.responseText);
          if (response.status === "error") {
            for (let fieldName in response.message) {
              let message = response.message[fieldName];
              let $inputField = $("#" + fieldName);
              $inputField.after(
                '<div class="error-message" style="color:red;">' +
                  message +
                  "</div>",
              );
            }
          }
        } else {
          console.log("Error: " + xhr.status + " - " + error);
        }
      },
    });
  });
});

// Log in validation

$(document).ready(function () {
  $("#loginForm").submit(function (e) {
    e.preventDefault();
    const formData = $(this).serialize();

    $.ajax({
      type: "POST",
      url: $(this).attr("action"),
      data: formData,
      dataType: "json",
      success: function (response) {
        if (response.status === "success") {
          const redirectUrl = $("#signUpForm").data("redirect-url");
          window.location.href = redirectUrl; // Redirect to home page
        }
      },
      error: function (xhr, status, error) {
        if (xhr.status === 401) {
          $("#loginError").text(xhr.responseJSON.message).show(); // Display error message from the server
        } else {
          console.error("Error: " + xhr.status + " - " + xhr.statusText);
          $("#loginError")
            .text("An unexpected error occurred. Please try again.")
            .show();
        }
      },
    });
  });
});

// Update user information validation

$(document).ready(function () {
  $("#editForm").submit(function (e) {
    e.preventDefault();
    const formData = $(this).serialize();

    $.ajax({
      type: "POST",
      url: $(this).attr("action"),
      data: formData,
      dataType: "json",
      success: function (response) {
        if (response.status === "success") {
          location.reload(); // Reload the page to reflect changes
        }
      },
      error: function (xhr, status, error) {
        $(".error-message").remove();
        if (xhr.status === 500) {
          console.error("Server Error: " + xhr.responseText);
          alert(
            "We're experiencing technical difficulties. Please try again later.",
          );
        } else if (xhr.status === 400) {
          const response = JSON.parse(xhr.responseText);
          // console.log(response) Debug
          if (response.status === "error") {
            $("#missingSocialError").hide();
            for (let fieldName in response.message) {
              if (fieldName == "missingSocialError") {
                $("#missingSocialError")
                  .text("At least one social handle is required")
                  .show();
              }
              let message = response.message[fieldName];
              let $inputField = $("#" + "edit_" + fieldName);
              $inputField.after(
                '<div class="error-message" style="color:red;">' +
                  message +
                  "</div>",
              );
            }
          }
        } else {
          console.log("Error: " + xhr.status + " - " + error);
        }
      },
    });
  });
});

// Changing password validation

$(document).ready(function () {
  $("#passwordForm").submit(function (e) {
    e.preventDefault();
    const formData = $(this).serialize();

    $.ajax({
      type: "POST",
      url: $(this).attr("action"),
      data: formData,
      dataType: "json",
      success: function (response) {
        if (response.status === "success") {
          location.reload();
        }
      },
      error: function (xhr) {
        $(".error-message").remove();
        if (xhr.status === 500) {
          console.error("Server Error: " + xhr.responseText);
          $("#passwordError")
            .text(
              "We're experiencing technical difficulties. Please try again later.",
            )
            .show();
        } else if (xhr.status === 400) {
          const response = JSON.parse(xhr.responseText);
          $("#passwordError").text(xhr.responseJSON.message).show();
        } else {
          console.error("Error: " + xhr.status + " - " + xhr.statusText);
        }
      },
    });
  });
});

function loadUserProfile(userId) {
  fetch(`/profile/${userId}`)
    .then((response) => response.json())
    .then((data) => {
      // Clear previous data
      document.getElementById("user-name").textContent =
        `${data.first_name} ${data.last_name}`;
      document.getElementById("user-email").textContent = data.email;
      document.getElementById("user-phone").textContent =
        data.phone_number || "N/A";

      // Checking if the social media information exists
      document.getElementById("user-instagram").textContent =
        data.socials.instagram || "N/A";
      document.getElementById("user-facebook").textContent =
        data.socials.facebook || "N/A";
      document.getElementById("user-snapchat").textContent =
        data.socials.snapchat || "N/A";
    })
    .catch((error) => {
      console.error("Error loading the user profile:", error);
      const modalBody = document.querySelector("#profileModal .modal-body");
      modalBody.innerHTML = `<p>Error loading profile. Please try again.</p>`; // Handle loading errors
    });
}

// ----- Replies -----

function setPostId(postId) {
  $("#post-id").val(postId); // Set the value of the input
}

function toggleReplies(postId) {
  $("#replies-" + postId).toggle(); // Toggle the display state of the replies
}

// Dynamically show the reply without refresching the page

$(document).ready(function () {
  $("#replyForm").submit(function (event) {
    event.preventDefault(); // Prevent the default form submission

    var formData = new FormData(this);
    var postUrl = $("#submitReplyUrl").val(); // Get the URL from the hidden input

    $.ajax({
      type: "POST",
      url: postUrl,
      data: formData,
      processData: false, // Prevent jQuery from converting the data into a query string
      contentType: false, // Must be false to tell jQuery not to add a Content-Type header
      success: function (data) {
        if (data.error) {
          alert(data.error);
        } else {
          console.log(data.message);
          $("#replyModal").modal("hide"); // Hide the modal using jQuery
          $('#replyForm textarea[name="content"]').val(""); // Clear the reply box

          // Dynamically add reply and immediatley show the current replies
          let replyHtml =
            '<div class="card mt-2"><div class="card-body">' +
            '<h6 class="card-subtitle mb-2 text-muted">Reply by You</h6>' +
            '<p class="card-text">' +
            data.content +
            "</p></div></div>";
          $("#replies-" + data.post_id)
            .prepend(replyHtml)
            .show();
        }
      },
      error: function (xhr, status, error) {
        if (xhr.status == 403) {
          $("#replyError").text("You need to be logged in to reply.").show(); // Update and show error div
        } else {
          $("#replyError").text("An error occurred. Please try again.").show(); // Handle other errors
        }
        console.error("Error:", error);
      },
    });
  });
});

// Falling hearts animation function
function createHeart() {
  const heart = document.createElement('div');
  heart.classList.add('heart');
  
  // Randomize position, size, and animation duration
  heart.style.left = Math.random() * 100 + 'vw';
  heart.style.animationDuration = Math.random() * 5 + 5 + 's'; // Varying speed
  heart.style.opacity = Math.random() * 0.5 + 0.5; // Random opacity between 0.5 and 1

  // Calculate fall height dynamically based on document height
  const fallHeight = document.body.scrollHeight + 'px';
  heart.style.setProperty('--fallHeight', fallHeight);

  document.body.appendChild(heart);

  // Remove heart after the animation is complete
  heart.addEventListener('animationend', () => {
    heart.remove();
  });
}


setInterval(createHeart, 1500);
