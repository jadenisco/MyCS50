from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import *

class ListingForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    description  = forms.CharField(label="Description", widget=forms.Textarea)
    bid = forms.DecimalField(label="Starting bid $", max_value=10000, min_value=0, decimal_places=2)
    categories = forms.ModelChoiceField(label="Category", queryset=Category.objects.all())


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
                bid = Bid(amount=float(form.data["bid"]))
                bid.save()

                listing = Listing(title=form.data["title"],
                                  description=form.data["description"])
                listing.save()

                auction = Auction(listing=listing)
                auction.save()
                auction.bids.add(bid)

                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponseBadRequest("Bad Request: Invalid Form")
    else:
        return HttpResponseRedirect(reverse("login"))
