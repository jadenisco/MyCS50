from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import *

class ListingForm(forms.Form):
    description = forms.CharField(label="Description", max_length=100)
    comment  = forms.CharField(label="Comment", widget=forms.Textarea)
    bid = forms.DecimalField(label="Starting bid (Dollars)", max_value=10000, min_value=0, decimal_places=2)


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    if request.user.is_authenticated:  
        if request.method == "GET":
            form = ListingForm()
            return render(request, "auctions/create.html", {
                "form": form
            })
        else:
            form = ListingForm(request.POST)
            if form.is_valid:
                description = form.data["description"]
                cf  = form.data["comment"]
                bf = form.data["bid"]

                comment = Comment(comment=cf)
                bid = Bid(amount=float(bf))
                listing = Listing(description=description)
                comment.save()
                bid.save()
                listing.save()
                
                listing.comments.add(comment)
                listing.bids.add(bid)
                
                # Add the listing to an auction
                
                # Add the auction to the user

                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponseBadRequest("Bad Request: Invalid Form")
    else:
        return HttpResponseRedirect(reverse("login"))
