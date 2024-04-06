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