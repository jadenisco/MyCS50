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


function set_like(post, json) {
  if (json.likes.includes(json.name)) {
    document.querySelector('#' + post).children[3].style.color = "red";
  } else {
    document.querySelector('#' + post).children[3].style.color = "black";
  }
  document.querySelector('#' + post).children[4].innerHTML = json.likes.length
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


function handleLikeClick(event) {
  post = event.target.parentNode.id;

  fetch('/like/' + post, {
    method: "PUT",
    headers: {
      "Content-type": "application/json; charset=UTF-8"
  }}).then(response => response.json())
  .then((json) => {
      if (json['error'] != null) {
        console.log("Like failed: " + putError);
      } else {
        set_like(post, json);
      }
  })
  
  // This is another way to handle the response
  //  .then(response => {
  //   j = response.json();
  //   s = response.status;
  //  })
  //  .catch(error => { console.log(error); return;})
  //  .then(json => { console.log(json) })
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

function render_paginator(page_obj, view) {
  contents = `<hr>
    <nav aria-label="Page navigation">
    <ul class="pagination pagination-sm justify-content-left">
  `;

  if (page_obj.page.has_previous) {
    contents += `<li class="page-item">
      <a class="page-link" href="?page=${ page_obj.page.current - 1 }">&laquo; Previous</a>
      </li>`;
  } else {
    contents += `<li class="page-item disabled">
      <a class="page-link" href="#" tabindex="-1" aria-disabled="true">&laquo; Previous</a>
    </li>`;
  }

  for (let i = 0; i < page_obj.page.range.length; i++) {
    p = page_obj.page.range[i];
    if (page_obj.page.current == p) {
      contents += `<li class="page-item active"><a class="page-link" href="?page=${p}}">${p}</a></li>`;
    } else {
      contents += `<li class="page-item"><a class="page-link" href="?page=${p}">${p}</a></li>`;
    }
  }

  if (page_obj.page.has_next) {
    contents += `<li class="page-item">
      <a class="page-link" href="?page=${ page_obj.page.current + 1 }">Next &raquo;</a>
      </li>`;
  } else {
    contents += `<li class="page-item disabled">
      <a class="page-link" href="#" tabindex="-1" aria-disabled="true">Next &raquo;</a>
    </li>`;
  }

  const paginatorView = document.createElement('div');
  paginatorView.id = 'paginator-view';
  paginatorView.innerHTML = contents;
  document.querySelector(view).append(paginatorView);
}


function render_posts(page_obj, postsView) {
  posts = page_obj.page.posts;

  posts.forEach((post, key) => {
    contents = `<div id="post-${post.id}">
      <a class="post-user" id="post-nm-${post.name}" href="#" onclick="handleProfileClick(event)"><strong>${post.name}</strong></a>`;

    if (document.getElementById(`profile-${post.name}`)) {
      contents += `<div><a class="post-edit" href="#" onclick="handleEditClick(event)">Edit</a></div>`
    };

    contents += `
      <p>${post.body}</p>
      <a style="color: red" href="#" onclick="handleLikeClick(event)">♥️ </a>
      <b style="color:grey">${post.likes}</b>
      <p style="color:grey">${post.timestamp}</p>
    </div>`;

    const postLink = document.createElement('div');
    postLink.className = 'post-link';
    postLink.innerHTML = contents;
    document.querySelector(postsView).append(postLink);
  })

  render_paginator(page_obj, postsView);
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

  document.querySelector('#paginator-view').remove()
  const profilePaginatorView = document.createElement('div');
  profilePaginatorView.id = 'paginator-view';
  document.querySelector('#profile-view').append(profilePostsView);

  render_profile_user(profile.user);
  render_posts(profile.page_obj, '#profile-posts-view');
}


function handleEditDeleteResponse(event) {
  pLink = event.target.parentNode.parentNode.parentNode;
  pLink.remove();
}


function handleEditSaveResponse(event, formBody) {
  pLink = event.target.parentNode.parentNode;
  post = pLink.children[0];
  text = post.children[2];

  text.innerHTML = formBody;
  post.hidden = false;
  pLink.children[1].remove();
}


function handleEditSaveSame(event) {
  pLink = event.target.parentNode.parentNode;
  pLink.children[0].hidden = false;
  pLink.children[1].remove();
}


function handleEditSave(event) {
  const post = event.target.parentNode;
  const text = post.parentNode.children[0].children[2].textContent;
  const formData = new FormData(event.target);
  const data={};
  const jsonBody={};

  formData.forEach((value, key) => (data[key] = value))
  jsonBody['post-id'] = `${post.id}`;
  jsonBody['type'] = "save";
  jsonBody['form'] = data;

  if (text == data['body']) {
    handleEditSaveSame(event);
  } else {
    fetch(`edit`, {
      method: "PUT",
      body: JSON.stringify(jsonBody),
      headers: {
        "Content-type": "application/json; charset=UTF-8"
      }}).then((response) => {
        console.log("Response Status: ", response.status);
        if(response.status == '201') {
          handleEditSaveResponse(event, data['body']);
        }  
      })  
  }
}


function handleEditDelete(event) {
  const post = event.target.parentNode.parentNode;
  const data={};
  const jsonBody={};

  jsonBody['post-id'] = `${post.id}`;
  jsonBody['type'] = "delete";

  fetch(`edit`, {
    method: "PUT",
    body: JSON.stringify(jsonBody),
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }}).then((response) => {
      console.log("Response Status: ", response.status);
      if(response.status == '201') {
          handleEditDeleteResponse(event);
      }  
    })  
}


function handleEditCancel(event) {
  pLink = event.target.parentNode.parentNode.parentNode;
  pLink.children[0].hidden = false;
  pLink.children[1].remove();
}


function handleEditClick(event) {
  const post = event.target.parentNode.parentNode;
  const pLink = post.parentNode;
  const newPost = document.createElement('div');
  const postText = post.children[2].getInnerHTML()

  contents = `<p>Edit Post</p><form id="compose-form" onsubmit="handleEditSave(event)">
    <textarea class="form-control" id="compose-body" name="body">${postText}</textarea>
    <input type="submit" value="Save" class="btn btn-primary btn-sm"/>
    <input type="button" value="Cancel" class="btn btn-primary btn-sm" onclick="handleEditCancel(event)"/>
    <input type="button" value="Delete" class="btn btn-primary btn-sm" onclick="handleEditDelete(event)"/>
    </form>`

  post.hidden = true;
  newPost.id = post.id
  newPost.innerHTML = contents;
  pLink.append(newPost);
}


function handleProfileClick(event) {
  let profile = '/profile/' + event.currentTarget.id + '/';
  let params = new URLSearchParams(document.location.search);
  let page = params.get("page");
  if (page) {
    url = profile + page;
  } else {
    url = profile + "1";
  }

  fetch(url)
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
  let params = new URLSearchParams(document.location.search);
  let page = params.get("page");
  if (page) {
    url = "following_posts/" + page;
  } else {
    url = "following_posts/" + "1";
  }

  fetch(url, {
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }})
    .then((response) => response.json())
    .then(page_obj => {render_posts(page_obj, '#following-posts-view')})
}


function load_posts() {
  let params = new URLSearchParams(document.location.search);
  let page = params.get("page");
  if (page) {
    url = "posts/" + page;
  } else {
    url = "posts/" + "1";
  }

  fetch(url, {
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }})
    .then((response) => response.json())
    .then(page_obj => {render_posts(page_obj, '#all-posts-posts-view')})
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
