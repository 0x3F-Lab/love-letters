$(document).ready(function () {
  // Toggle Edit and Password forms
  $("#editButton").click(function () {
    $("#editFormDiv").toggle();
  });

  $("#changePasswordButton").click(function () {
    $("#passwordFormDiv").toggle();
  });

  // Sign-up Form validation
  $("#signUpForm").submit(function (e) {
    e.preventDefault(); // Prevent default form submission
    const formData = $(this).serialize(); // Serialize form data

    $.post($(this).attr("action"), formData, function (response) {
      const redirectUrl = $("#signUpForm").data("redirect-url");
      window.location.href = redirectUrl; // Redirect to home page
    }).fail(function (xhr) {
      $(".error-message").remove(); // Clear previous error messages

      if (xhr.status === 500) {
        alert(
          "We're experiencing technical difficulties. Please try again later.",
        );
      } else if (xhr.status === 400) {
        const response = xhr.responseJSON;
        if (response.status === "error") {
          $.each(response.message, function (fieldName, message) {
            $("#" + fieldName).after(
              '<div class="error-message" style="color:red;">' +
                message +
                "</div>",
            );
          });
        }
      } else {
        console.log("Error: " + xhr.status + " - " + xhr.statusText);
      }
    });
  });

  // Log in validation
  $("#loginForm").submit(function (e) {
    e.preventDefault();
    const formData = $(this).serialize();

    $.post($(this).attr("action"), formData, function (response) {
      if (response.status === "success") {
        const redirectUrl = $("#signUpForm").data("redirect-url");
        window.location.href = redirectUrl; // Redirect to home page
      }
    }).fail(function (xhr) {
      if (xhr.status === 401) {
        $("#loginError").text(xhr.responseJSON.message).show();
      } else {
        $("#loginError")
          .text("An unexpected error occurred. Please try again.")
          .show();
      }
    });
  });

  // Update user information validation
  $("#editForm").submit(function (e) {
    e.preventDefault();
    const formData = $(this).serialize();

    $.post($(this).attr("action"), formData, function (response) {
      if (response.status === "success") {
        location.reload();
      }
    }).fail(function (xhr) {
      $(".error-message").remove();
      if (xhr.status === 500) {
        alert(
          "We're experiencing technical difficulties. Please try again later.",
        );
      } else if (xhr.status === 400) {
        const response = xhr.responseJSON;
        if (response.status === "error") {
          $("#missingSocialError").hide();
          $.each(response.message, function (fieldName, message) {
            if (fieldName == "missingSocialError") {
              $("#missingSocialError")
                .text("At least one social handle is required")
                .show();
            }
            $("#edit_" + fieldName).after(
              '<div class="error-message" style="color:red;">' +
                message +
                "</div>",
            );
          });
        }
      } else {
        console.log("Error: " + xhr.status + " - " + xhr.statusText);
      }
    });
  });

  // Change password validation
  $("#passwordForm").submit(function (e) {
    e.preventDefault();
    const formData = $(this).serialize();

    $.post($(this).attr("action"), formData, function (response) {
      if (response.status === "success") {
        location.reload();
      }
    }).fail(function (xhr) {
      $(".error-message").remove();
      if (xhr.status === 500) {
        $("#passwordError")
          .text(
            "We're experiencing technical difficulties. Please try again later.",
          )
          .show();
      } else if (xhr.status === 400) {
        $("#passwordError").text(xhr.responseJSON.message).show();
      } else {
        console.log("Error: " + xhr.status + " - " + xhr.statusText);
      }
    });
  });

  // Load user profile
  window.loadUserProfile = function (userId) {
    fetch(`/profile/${userId}`)
      .then((response) => response.json())
      .then((data) => {
        $("#user-name").text(`${data.first_name} ${data.last_name}`);
        $("#user-email").text(data.email);
        $("#user-phone").text(data.phone_number || "N/A");
        $("#user-gender").text(data.gender || "Not provided");
        $("#user-instagram").text(data.socials.instagram || "N/A");
        $("#user-facebook").text(data.socials.facebook || "N/A");
        $("#user-snapchat").text(data.socials.snapchat || "N/A");

        $("#user-instagram-link").attr(
          "href",
          data.socials.instagram
            ? `https://instagram.com/${data.socials.instagram}`
            : "#",
        );
        $("#user-facebook-link").attr(
          "href",
          data.socials.facebook
            ? `https://facebook.com/${data.socials.facebook}`
            : "#",
        );
        $("#user-snapchat-link").attr(
          "href",
          data.socials.snapchat
            ? `https://snapchat.com/add/${data.socials.snapchat}`
            : "#",
        );

        $("#profileModal").modal("show");
      })
      .catch((error) => {
        console.error("Error loading the user profile:", error);
        $("#profileModal .modal-body").html(
          "<p>Error loading profile. Please try again.</p>",
        );
        $("#profileModal").modal("show");
      });
  };

  // Replies
  window.setPostId = function (postId) {
    $("#post-id").val(postId);
  };

  window.toggleReplies = function (postId) {
    $("#replies-" + postId).toggle();
  };

  // Dynamically show the reply without refreshing the page
  $("#replyForm").submit(function (event) {
    event.preventDefault();
    var formData = new FormData(this);
    var postUrl = $("#submitReplyUrl").val();

    $.ajax({
      type: "POST",
      url: postUrl,
      data: formData,
      processData: false,
      contentType: false,
      success: function (data) {
        if (data.error) {
          alert(data.error);
        } else {
          $("#replyModal").modal("hide");
          $('#replyForm textarea[name="content"]').val("");

          let replyHtml = `<div class="card mt-2"><div class="card-body"><h6 class="card-subtitle mb-2 text-muted">Reply by You</h6><p class="card-text">${data.content}</p></div></div>`;
          $("#replies-" + data.post_id)
            .prepend(replyHtml)
            .show();
        }
      },
      error: function (xhr) {
        console.error("Error:", xhr.responseText);
        if (xhr.status == 403) {
          $("#replyError").text("You need to be logged in to reply.").show();
          $("#replyModal")
            .modal("hide")
            .on("hidden.bs.modal", function () {
              $("#loginModal").modal("show");
              $(this).off("hidden.bs.modal");
            });
        } else {
          $("#replyError").text("An error occurred. Please try again.").show();
        }
      },
    });
  });

  // Like post
  window.toggleLikePost = function (postId) {
    var csrfToken = $("#csrf_token").val();
    $.post(
      "/post/like_post",
      { post_id: postId, csrf_token: csrfToken },
      function (response) {
        var likeButton = $(`.like-btn[data-post-id="${postId}"]`);
        if (response.status === "unlike") {
          likeButton.html(
            `Unlike (<span id="like-count-${postId}">${response.count}</span>)`,
          );
        } else {
          likeButton.html(
            `Like (<span id="like-count-${postId}">${response.count}</span>)`,
          );
        }
      },
    ).fail(function (xhr) {
      console.log(
        xhr.responseJSON && xhr.responseJSON.error
          ? xhr.responseJSON.error
          : "An error occurred",
      );
    });
  };

  // Like reply
  window.toggleLikeReply = function (replyId) {
    var csrfToken = $("#csrf_token").val();
    $.post(
      "/post/like_reply",
      { reply_id: replyId, csrf_token: csrfToken },
      function (response) {
        var likeButton = $(`.like-btn[data-reply-id="${replyId}"]`);
        var likeCount = $(`#like-count-reply-${replyId}`);
        if (response.status === "unlike") {
          likeButton.html(`Unlike (${response.count})`);
        } else {
          likeButton.html(`Like (${response.count})`);
        }
      },
    ).fail(function (xhr) {
      console.error("An error occurred:", xhr.responseText);
      alert("Failed to like the reply. Please try again.");
    });
  };

  // Load more posts on scroll
  var page = 1;
  var loading = false;
  var debounceTimer;
  var allPostsLoaded = false;
  var footerVisible = true;

  function loadMorePosts() {
    if (loading || allPostsLoaded) return;
    loading = true;
    displaySkeletons(5);

    const sort = $('select[name="sort"]').val();

    setTimeout(() => {
      $.get(`/post/browse/${page + 1}?sort=${sort}`, function (data) {
        if (data.posts.length > 0) {
          $(".posts-container").append(data.posts);
          $(".card-animation").css("opacity", "1");
          page += 1;
        } else {
          allPostsLoaded = true;
        }
      })
        .fail(function (error) {
          console.error("Error loading posts:", error);
        })
        .always(function () {
          removeSkeletons();
          loading = false;
        });
    }, 600);
  }

  function displaySkeletons(count) {
    const container = $(".posts-container");
    const skeletonTemplate = $("#skeleton-template").html();
    for (let i = 0; i < count; i++) {
      container.append(skeletonTemplate);
    }
  }

  function removeSkeletons() {
    $(".post-skeleton").remove();
  }

  function handleScroll() {
    if (debounceTimer) {
      clearTimeout(debounceTimer);
    }
    debounceTimer = setTimeout(() => {
      const scrollPosition = $(window).scrollTop() + $(window).height();
      const totalHeight = $(document).height();
      const threshold = 300;
      if (scrollPosition >= totalHeight - threshold && !loading) {
        loadMorePosts();
        if (footerVisible) {
          $("#page-footer").hide();
          footerVisible = false;
        }
      }
    }, 100);
  }

  $(window).on("scroll", handleScroll);

  // Card animation on load
  $(".card-animation").each(function (index) {
    setTimeout(() => {
      $(this).addClass("card-slide-in");
    }, 100 * index);
  });

  // Animated text
  let phrases = [
    "Find love or friendship!",
    "Connect with others!",
    "Share your story!",
  ];
  let currentIndex = 0;

  function updateText() {
    $("#animatedText").fadeOut(function () {
      $(this).text(phrases[currentIndex]).fadeIn();
    });

    currentIndex = (currentIndex + 1) % phrases.length;
  }

  setInterval(updateText, 3000);

  // Swipe cards
  let isDragging = false;
  let startX, startY;

  $(document).on("mousedown touchstart", ".author-link", function (e) {
    e.stopPropagation();
  });

  $(document).on("mousedown touchstart", ".swipe-card", function (e) {
    e.preventDefault();
    isDragging = true;
    let card = $(this);

    startX = e.pageX || e.originalEvent.touches[0].pageX;
    startY = e.pageY || e.originalEvent.touches[0].pageY;

    $(document).on("mousemove touchmove", function (e) {
      if (!isDragging) return;
      let moveX = e.pageX || e.originalEvent.touches[0].pageX;
      let moveY = e.pageY || e.originalEvent.touches[0].pageY;
      let diffX = moveX - startX;
      let diffY = moveY - startY;

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

      if (Math.sqrt(diffX * diffX + diffY * diffY) > 200) {
        card.animate(
          {
            transform: `translateX(${diffX > 0 ? "1000px" : "-1000px"})`,
            opacity: 0,
          },
          300,
          function () {
            card.remove();
            if ($(".swipe-card").length === 0) {
              $("#swipe-text").html(
                "<p class='text-center'>No more posts to swipe through</p>",
              );
            }
          },
        );
      } else {
        card.css({
          transform: "translateX(-50%) translateY(0)",
          cursor: "grab",
        });
      }
    });
  });
});
