from django.urls import path
from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("random", views.random_page, name="random"),
    path("edit", views.edit, name="edit"),
    path("<str:title>", views.entry, name="entry"),
]
