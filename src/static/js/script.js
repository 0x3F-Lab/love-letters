// ----------   USER PROFILE ----------

$(document).ready(function () {
  $("#editButton").click(function () {
    $("#editForm").toggle();
  });

  $("#changePasswordButton").click(function () {
    $("#passwordForm").toggle();
  });
});


function setPostId(postId) {
    document.getElementById('post-id').value = postId;
}

