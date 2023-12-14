from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("watchlistadd/<int:listing_id>", views.watchlistadd, name="watchlistadd"),
    path("watchlistremove/<int:listing_id>", views.watchlistremove, name="watchlistremove"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("close/<int:listing_id>", views.close, name="close")
]
