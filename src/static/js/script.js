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

          // Dynamically add reply and immediately show the current replies
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
        console.error("Error:", error); // Log any errors to the console
        if (xhr.status == 403) {
          $("#replyError").text("You need to be logged in to reply.").show(); // Update and show error div
          $("#replyModal")
            .modal("hide")
            .on("hidden.bs.modal", function () {
              $("#loginModal").modal("show"); // Show login modal only after reply modal has hidden
              $(this).off("hidden.bs.modal"); // Remove the event handler to avoid stacking handlers
            });
        } else {
          $("#replyError").text("An error occurred. Please try again.").show(); // Handle other errors
        }
      },
    });
  });
});

function toggleLikePost(postId, userId) {
  var csrfToken = $("#csrf_token").val();
  $.ajax({
    url: "/post/like_post",
    type: "POST",
    data: { post_id: postId, user_id: userId, csrf_token: csrfToken },
    success: function (response) {
      var likeButton = $('.like-btn[data-post-id="' + postId + '"]');
      if (response.status === "unlike") {
        // If the response says 'unlike', it means the post is now liked
        likeButton.html(
          'Unlike (<span id="like-count-' +
            postId +
            '">' +
            response.count +
            "</span>)",
        );
      } else {
        // If the response says 'like', it means the post is now unliked
        likeButton.html(
          'Like (<span id="like-count-' +
            postId +
            '">' +
            response.count +
            "</span>)",
        );
      }
    },
    error: function (xhr) {
      console.log(
        xhr.responseJSON && xhr.responseJSON.error
          ? xhr.responseJSON.error
          : "An error occurred",
      );
    },
  });
}

function toggleLikeReply(replyId, userId) {
  var csrfToken = $("#csrf_token").val();
  $.ajax({
    url: "/post/like_reply",
    type: "POST",
    data: { reply_id: replyId, user_id: userId, csrf_token: csrfToken },
    success: function (response) {
      var likeButton = $('.like-btn[data-reply-id="' + replyId + '"]');
      var likeCount = $("#like-count-reply-" + replyId);
      if (response.status === "unlike") {
        // If currently liked, show unlike
        likeButton.html("Unlike (" + response.count + ")");
      } else {
        // If currently unliked, show like
        likeButton.html("Like (" + response.count + ")");
      }
    },
    error: function (xhr) {
      console.error("An error occurred:", xhr.responseText);
      alert("Failed to like the reply. Please try again.");
    },
  });
}

document.addEventListener("DOMContentLoaded", function() {
  let page = 1;
  let loading = false;
  let debounceTimer;
  let allPostsLoaded = false;
  let footerVisible = true; // Track the visibility of the footer

  function loadMorePosts() {
if (loading || allPostsLoaded) return;
loading = true;
displaySkeletons(5);

const sort = document.querySelector('select[name="sort"]').value; // Get current sort order

setTimeout(() => {
  fetch(`/post/browse/${page + 1}?sort=${sort}`, { // Include sort parameter
      headers: { 'X-Requested-With': 'XMLHttpRequest' }
  })
  .then(response => response.json())
  .then(data => {
      if (data.posts.length > 0) {
          const container = document.querySelector('.container');
          container.insertAdjacentHTML('beforeend', data.posts);
          page += 1;
      } else {
          allPostsLoaded = true;
      }
  })
  .catch(error => {
      console.error('Error loading posts:', error);
  })
  .finally(() => {
      removeSkeletons();
      loading = false;
  });
}, 600);
}

  function displaySkeletons(count) {
      const container = document.querySelector('.container');
      const skeletonTemplate = document.getElementById('skeleton-template').content;
      for (let i = 0; i < count; i++) {
          container.appendChild(document.importNode(skeletonTemplate, true));
      }
  }

  function removeSkeletons() {
      document.querySelectorAll('.post-skeleton').forEach(skeleton => skeleton.remove());
  }

  function handleScroll() {
      if (debounceTimer) {
          clearTimeout(debounceTimer);
      }
      debounceTimer = setTimeout(() => {
          const scrollPosition = window.scrollY + window.innerHeight;
          const totalHeight = document.body.scrollHeight;
          const threshold = 300;
          if (scrollPosition >= totalHeight - threshold && !loading) {
              loadMorePosts();
              if (footerVisible) {
                  document.getElementById('page-footer').style.display = 'none'; // Hide the footer
                  footerVisible = false; // Update the visibility flag
              }
          }
      }, 100);
  }

  window.addEventListener('scroll', handleScroll);
});