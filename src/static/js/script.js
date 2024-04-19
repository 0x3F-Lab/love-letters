// ----------   USER PROFILE ----------

$(document).ready(function () {
  $("#editButton").click(function () {
    $("#editForm").toggle();
  });

  $("#changePasswordButton").click(function () {
    $("#passwordForm").toggle();
  });
});

function loadUserProfile(userId) {
  fetch(`/profile/${userId}`)
      .then(response => response.json())
      .then(data => {
          const modalBody = document.querySelector('#profileModal .modal-body');
          modalBody.innerHTML = `<p>Name: ${data.first_name} ${data.last_name}</p>
                                 <p>Email: ${data.email}</p>
                                 <p>Phone: ${data.phone_number}</p>
                                 <p>Instagram: ${data.socials.instagram || 'N/A'}</p>
                                 <p>Facebook: ${data.socials.facebook || 'N/A'}</p>
                                 <p>Snapchat: ${data.socials.snapchat || 'N/A'}`;
      })
      .catch(error => console.error('Error loading the user profile:', error));
}