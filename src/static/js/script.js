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

// $(document).ready(function () {
//   $(".swipe-card").each(function() { // Ensure each card sets up its own handlers
//     let isDragging = false;
//     let startX, startY;
//     let card = $(this); // Reference to the current card

//     card.on("mousedown touchstart", function (e) {
//       e.preventDefault();
//       isDragging = true;

//       startX = e.pageX || e.originalEvent.touches[0].pageX;
//       startY = e.pageY || e.originalEvent.touches[0].pageY;

//       // Attach move and end handlers directly to the card
//       card.on("mousemove touchmove", function (e) {
//         if (!isDragging) return;
//         let moveX = e.pageX || e.originalEvent.touches[0].pageX;
//         let moveY = e.pageY || e.originalEvent.touches[0].pageY;
//         let diffX = moveX - startX;
//         let diffY = moveY - startY;

//         card.css({
//           transform: `translateX(calc(-50% + ${diffX}px)) translateY(${diffY}px)`,
//           cursor: 'grabbing'
//         });
//       });

//       card.on("mouseup touchend", function (e) {
//         card.off("mousemove touchmove"); // Unbind move event
//         isDragging = false;

//         let endX = e.pageX || e.changedTouches[0].pageX;
//         let diffX = endX - startX;

//         if (Math.abs(diffX) > 150) {
//           if (diffX > 0) { // Swipe right
//             $.ajax({
//               url: card.find('.connect-form').attr('action'),
//               type: 'POST',
//               data: card.find('.connect-form').serialize(),
//               success: function(response) {
//                 // alert('Connection request sent!');
//               },
//               error: function(xhr, status, error) {
//                 // alert('Failed to send request!');
//               }
//             });
//           }
//           card.animate({
//             transform: `translateX(${diffX > 0 ? '1000px' : '-1000px'})`,
//             opacity: 0
//           }, 300, function() {
//             card.remove();
//           });
//         } else {
//           card.css({
//             transform: 'translateX(-50%) translateY(0px)',
//             cursor: 'grab'
//           });
//         }
//         card.off("mouseup touchend"); // Unbind this event after execution
//       });
//     });
//   });
// });

$(document).ready(function () {
  let isDragging = false;
  let startX, startY;

  $(".swipe-card").on("mousedown touchstart", function (e) {
    e.preventDefault();
    isDragging = true;
    let card = $(this);

    // Get the starting point of the touch/drag
    startX = e.pageX || e.originalEvent.touches[0].pageX;
    startY = e.pageY || e.originalEvent.touches[0].pageY;

    $(document).on("mousemove touchmove", function (e) {
      if (!isDragging) return;
      let moveX = e.pageX || e.originalEvent.touches[0].pageX;
      let moveY = e.pageY || e.originalEvent.touches[0].pageY;
      let diffX = moveX - startX;
      let diffY = moveY - startY;

      // Use translate for movement keeping the initial centering
      card.css({
        transform: `translateX(calc(-50% + ${diffX}px)) translateY(${diffY}px)`,
        cursor: "grabbing",
      });
    });

    $(document).on("mouseup touchend", function (e) {
      $(document).off("mousemove touchmove");
      isDragging = false;

      let endX = e.pageX || e.changedTouches[0].pageX;
      let endY = e.pageY || e.changedTouches[0].pageY;
      let diffX = endX - startX;
      let diffY = endY - startY;

      // Check distance for snapping or resetting
      if (Math.sqrt(diffX * diffX + diffY * diffY) > 200) {
        card.animate(
          {
            transform: `translateX(${diffX > 0 ? "1000px" : "-1000px"})`,
            opacity: 0,
          },
          300,
          function () {
            card.remove();
          },
        );
      } else {
        // Reset to the original position with transform
        card.css({
          transform: "translateX(-50%)",
          cursor: "grab",
        });
      }
    });
  });
});
