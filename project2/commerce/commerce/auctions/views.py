from django.shortcuts import render
from django.urls import reverse

from .models import Auction, Listing, Profile


def index(request):
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.all(),
        "listings": Listing.objects.all(),
        "profiles": Profile.objects.all()
    })


def auction(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    return render(request, "auctions/auction.html", {
        "auction": auction        
    })

