document.addEventListener('DOMContentLoaded', function() {

  render_all_posts()
})


function render_all_posts() {
  document.querySelector('#all-posts-view').style.display = 'block';
  document.querySelector('#profile-view').style.display = 'none';

  load_posts();
}


function render_profile_user(profileUser) {
  console.log(render_profile_user);

  contents = `<div style="display: flex; align-items: center;">
    <div><h3 style="margin-right: 15px;">${profileUser.username}:</h3></div>
      <div><h5>${profileUser.email}</h5></div>
    </div>`;

  if (profileUser.requestor != profileUser.username) {
    contents += `<button type="button" class="btn btn-secondary btn-sm">Unfollow</button>`;
    contents += `<button type="button" class="btn btn-primary btn-sm">Follow</button>`;
  }

  const profile = document.createElement('div');
  profile.className = 'profile-user-view';
  profile.innerHTML = contents;
  document.querySelector('#profile-user').append(profile);
}

function render_posts(posts, postsView) {

  posts.forEach((post, key) => {

    console.log("key: %s id: %s", key, post.id);
    contents = `<div id="post-${post.id}">
      <div id="profile-${post.name}" onclick="handleProfileClick(event)">
        <h5>${post.name}</h5>
      </div>
      <p>Edit</p>
      <p>${post.body}</p>
      <p style="color: red">♥️ <b style="color:grey">${post.likes}</b></p>
      <p style="color:grey">${post.timestamp}</p>
      <p>Comment</p>
    </div>`;

    const postLink = document.createElement('div');
    postLink.className = 'post-link';
    postLink.innerHTML = contents;
    document.querySelector(postsView).append(postLink);
  })
}


function render_profile (profile) {
  document.querySelector('#all-posts-view').style.display = 'none';
  document.querySelector('#profile-view').style.display = 'block';

  document.querySelector('#profile-user').remove();
  const profileUser = document.createElement('div');
  profileUser.id = 'profile-user';
  document.querySelector('#profile-view').append(profileUser);
  
  document.querySelector('#profile-posts-view').remove()
  const profilePostsView = document.createElement('div');
  profilePostsView.id = 'profile-posts-view';
  document.querySelector('#profile-view').append(profilePostsView);

  render_profile_user(profile.user);
  render_posts(profile.posts, '#profile-posts-view');
}


function handleProfileClick(event) {
  console.log("handleProfileClick")

  fetch(`/profile/${event.currentTarget.id}`)
  .then(response => response.json())
  .then(profile => {
    if (profile['error']) {
      console.error('Profile was not found!')
    } else {
      console.log(profile);
      render_profile(profile);
    }
  })
}


function load_posts() {
    fetch("posts", {
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
      })
      .then((response) => response.json())
      .then(posts => {render_posts(posts, '#all-posts-view')})
}


function post_form(event) {
    const formData = new FormData(event.target);
    const data={}

    formData.forEach((value, key) => (data[key] = value))
    fetch("post", {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        "Content-type": "application/json; charset=UTF-8"
      }
    })
    .then((response) => response.text())
    .then(text => console.log(text))
}
