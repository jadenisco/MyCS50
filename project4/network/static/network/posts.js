document.addEventListener('DOMContentLoaded', function() {

  if (this.location.pathname == '/following') {
    render_following();
  } else {
    render_all_posts();
  }
})


function render_all_posts() {
  document.querySelector('#all-posts-view').style.display = 'block';
  document.querySelector('#profile-view').style.display = 'none';
  document.querySelector('#following-view').style.display = 'none';
  load_posts();
}


function render_following() {
  document.querySelector('#all-posts-view').style.display = 'none';
  document.querySelector('#profile-view').style.display = 'none';
  document.querySelector('#following-view').style.display = 'block';
  load_following_posts();
}


function toggle_follow() {
  text = document.querySelector('.profile-user-view').children[1].textContent;
  if (text == 'Follow') {
    document.querySelector('.profile-user-view').children[1].textContent = 'Unfollow';
    document.querySelector('.profile-user-view').children[1].className = "btn btn-secondary btn-sm"
  } else {
    document.querySelector('.profile-user-view').children[1].textContent = 'Follow';
    document.querySelector('.profile-user-view').children[1].className = "btn btn-primary btn-sm"
  }
}


function handleFollowClick(profileUser) {
  if (profileUser.followers.includes(profileUser.requestor)) {
    jsonBody = JSON.stringify({follow: false});
  } else {
    jsonBody = JSON.stringify({follow: true});
  }

  fetch(`/follow/${profileUser.username}`, {
    method: "PUT",
    body: jsonBody,
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }
  }).then((response) => {
    console.log("Response Status: ", response.status);
    if(response.status == '204') {
      toggle_follow();
    }
  })
}


function render_profile_user(profileUser) {
  contents = `<div style="display: flex; align-items: center;">
    <div><h3 style="margin-right: 15px;">${profileUser.username}:</h3></div>
      <div><h5>${profileUser.email}</h5></div>
    </div>`;

  if (profileUser.requestor != profileUser.username) {
    if (profileUser.followers.includes(profileUser.requestor)) {
      contents += `<button type="button" class="btn btn-secondary btn-sm" id="follow-button">Unfollow</button>`;
    } else {
      contents += `<button type="button" class="btn btn-primary btn-sm" id="follow-button">Follow</button>`;
    }
  }

  const profile = document.createElement('div');
  profile.className = 'profile-user-view';
  profile.innerHTML = contents;
  document.querySelector('#profile-user').append(profile);

  if (profileUser.requestor != profileUser.username) {
    document.querySelector('#follow-button').addEventListener('click', () => handleFollowClick(profileUser));
  }
}


function render_posts(posts, postsView) {

  posts.forEach((post, key) => {
    contents = `<div id="post-${post.id}">
      <a class="post-user" id="profile-${post.name}" href="#" onclick="handleProfileClick(event)"><strong>${post.name}</strong></a>
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
  document.querySelector('#following-view').style.display = 'none';

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
  fetch(`/profile/${event.currentTarget.id}`)
  .then(response => response.json())
  .then(profile => {
    if (profile['error']) {
      console.error('Profile was not found!')
    } else {
      render_profile(profile);
    }
  })
}


function load_following_posts() {
  fetch("following_posts", {
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }})
    .then((response) => response.json())
    .then(posts => {render_posts(posts, '#following-view')})
}


function load_posts() {
  fetch("posts", {
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }})
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
    }})
    .then((response) => response.text())
    .then(text => console.log(text))
}
