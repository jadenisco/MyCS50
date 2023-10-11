from django.urls import path

from . import views

urlpatterns = [
    path("wiki", views.index, name="index")
]
