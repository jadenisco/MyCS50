
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("scratch", views.scratch, name="scratch"),
    path("following", views.index, name="following"),
    path("following_posts", views.following_posts, name="following_posts"),
    path("post", views.post, name="post"),
    path("profile/<str:name>", views.profile, name="profile"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("posts/<int:page>", views.posts, name="posts"),
]
