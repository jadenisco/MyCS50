document.addEventListener('DOMContentLoaded', function() {

  render_all_posts()
})


function render_all_posts() {
  document.querySelector('#all-posts-view').style.display = 'block';
  document.querySelector('#new-post-view').style.display = 'block';

  load_posts();
}


function render_posts(posts) {

  posts.forEach((post, key) => {

    console.log("key: %s id: %s", key, post.id);
    contents = `<div id="post-link-${post.id}"
      <h3>${post.name}</h3>
      <p>Edit</p>
      <p>${post.body}</p>
      <p style="color: red">♥️ <b style="color:grey">${post.likes}</b></p>
      <p style="color:grey">${post.timestamp}</p>
      <p>Comment</p>
    </div>`

    const postLink = document.createElement('div')
    postLink.className = 'post-link';
    postLink.innerHTML = contents;
    document.querySelector('#posts-view').append(postLink);
  })
}

function load_posts() {

    fetch("posts", {
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
      })
      .then((response) => response.json())
      .then(posts => {render_posts(posts)})
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
  