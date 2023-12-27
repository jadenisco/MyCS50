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
    bid = forms.DecimalField(label="Starting bid $", max_value=10000, min_value=0, decimal_places=0)
    category = forms.ModelChoiceField(label="Category", required=False, queryset=Category.objects.all())
    image = forms.ImageField(label="Image", required=False, widget=forms.URLInput)


class CommentForm(forms.Form):
    comment = forms.CharField(label="Comment", widget=forms.Textarea(attrs={'rows':4, 'cols':15}))


def _active_auctions():
    active_auctions = []
    for a in Auction.objects.all():
        if a.active:
            active_auctions.append(a)
    return active_auctions


def close(request, listing_id):
    user = request.user
    if user.is_authenticated:
        listing = Listing.objects.get(pk=listing_id)
        auction = listing.auction_listing
        auction.active = False
        auction.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id, )))
    else:
        return HttpResponseRedirect(reverse("login"))


def comment(request, listing_id):
    user = request.user
    if user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid:
            comment = Comment(username=user.username, comment=form.data['comment'])
            comment.save()   
            listing = Listing.objects.get(pk=listing_id)
            listing.comments.add(comment)
            listing.save()

            return HttpResponseRedirect(reverse("listing", args=(listing_id, )))
        else:
            return HttpResponseBadRequest("Bad Request: Invalid Form")
    else:
        return HttpResponseRedirect(reverse("login"))


def bid(request, listing_id):
    user = request.user
    if user.is_authenticated:
        listing = Listing.objects.get(pk=listing_id)
        auction = listing.auction_listing
        bid = Bid(user_id=user.id, amount=float(request.POST['bid']))
        bid.save()
        listing.high_bid = bid
        listing.save()
        auction.bids.add(bid)
        return HttpResponseRedirect(reverse("listing", args=(listing_id, )))
    else:
        return HttpResponseRedirect(reverse("login"))


def watchlist(request):
    print("watchlist")


def watchlistremove(request, listing_id):
    user = request.user
    if user.is_authenticated:
        listing = Listing.objects.get(pk=listing_id)
        if listing.auction_listing in user.watch_list.all():
            user.watch_list.remove(listing.auction_listing)
        return HttpResponseRedirect(reverse("listing", args=(listing_id, )))
    else:
        return HttpResponseRedirect(reverse("login"))


def watchlistadd(request, listing_id):
    user = request.user
    if user.is_authenticated:
        listing = Listing.objects.get(pk=listing_id)
        if listing.auction_listing not in user.watch_list.all():
            user.watch_list.add(listing.auction_listing)
        return HttpResponseRedirect(reverse("listing", args=(listing_id, )))
    else:
        return HttpResponseRedirect(reverse("login"))


def listing(request, listing_id):
    user = request.user
    if user.is_authenticated:
        listing = Listing.objects.get(pk=listing_id)
        auction = listing.auction_listing
        auction_user = User.objects.get(pk=auction.user_id)
        high_bid_user = User.objects.get(pk=listing.high_bid.user_id)
        commentform = CommentForm()
        return render(request, "auctions/listing.html", {
            "auction_user": auction_user,
            "listing": listing,
            "watchlist": user.watch_list.all(),
            "min_bid": listing.high_bid.amount + 1,
            "high_bid_user": high_bid_user,
            "commentform": commentform
        })
    else:
        return HttpResponseRedirect(reverse("login"))


def create(request):
    user = request.user
    if user.is_authenticated:  
        if request.method == "GET":
            form = ListingForm()
            return render(request, "auctions/create.html", {
                "form": form
            })
        else:
            form = ListingForm(request.POST)
            if form.is_valid:
                bid = Bid(user_id=user.id, amount=float(form.data["bid"]))
                bid.save()

                listing = Listing(title=form.data["title"],
                                  description=form.data["description"],
                                  high_bid=bid)
                ctg = form.data['category']
                img = form.data['image']
                if img != '':
                    listing.image = img
                listing.save()
                if ctg != '':
                    listing.category.add(Category.objects.get(id=int(ctg)))

                auction = Auction(user_id=user.id, listing=listing)
                auction.save()
                auction.bids.add(bid)

                user.auctions.add(auction.id)

                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponseBadRequest("Bad Request: Invalid Form")
    else:
        return HttpResponseRedirect(reverse("login"))


def index(request):
    user = request.user
    if user.is_authenticated:
        return render(request,"auctions/index.html", {
                                "authenticated": True,
                                "all": _active_auctions(),
                                "bids" : user.user_bids.all(),
                                "auctions" : user.auctions.all()}
                       )
    else:
        return render(request,"auctions/index.html", {
                                "authenticated": False,
                                "all": _active_auctions(),
                                "bids" : None,
                                "auctions" : None})


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
