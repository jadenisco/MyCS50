document.addEventListener('DOMContentLoaded', function() {

    load_new_post();

    load_posts('All Posts');

})

function load_new_post() {
    console.log("load_new_post")

    document.querySelector('#new-post-view').style.display = 'block';
}

function load_posts(title) {
    console.log("load_posts: %s", title)

    document.querySelector('#posts-view').style.display = 'block';

    document.querySelector('#posts-view').innerHTML = `<h3>${title}</h3>`;

}

function post_form(event) {
    console.log("post_form event.target: " + event.target)
  
    const formData = new FormData(event.target);
    const data={}
    formData.forEach((value, key) => (data[key] = value))
    console.log(data);
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
  