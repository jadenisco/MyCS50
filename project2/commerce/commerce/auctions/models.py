from django.contrib.auth.models import AbstractUser
from django.db import models
from djmoney.models.fields import MoneyField


class Category(models.Model):
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.description}"


class Comment(models.Model):
    username = models.CharField(max_length=64)
    comment = models.CharField(max_length=64)

    def __str__(self):
        return f"ID: {self.id}, Comment: {self.comment}"


class Bid(models.Model):
    user_id = models.IntegerField()
    amount = models.DecimalField(max_digits=10000, decimal_places=0)

    def __str__(self):
        return f"ID: {self.id}, Amount: {self.amount}"


class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    image = models.URLField(blank=True)
    category = models.ManyToManyField(Category, blank=True, related_name="categories")
    comments  = models.ManyToManyField(Comment, blank=True,related_name="comments")
    high_bid = models.OneToOneField(Bid, on_delete=models.CASCADE, related_name="high_bid")

    def __str__(self):
        return f"ID: {self.id}, Title: {self.title}"


class Auction(models.Model):
    user_id = models.IntegerField()
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE, related_name="auction_listing")
    bids = models.ManyToManyField(Bid, blank=True, related_name="auction_bids")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"ID: {self.id} Listing: {self.listing.title}"


class User(AbstractUser):
    auctions = models.ManyToManyField(Auction, blank=True, related_name="user_auctions")
    user_bids = models.ManyToManyField(Bid, blank=True, related_name="user_bids")
    watch_list = models.ManyToManyField(Auction, blank=True, related_name="user_watch_list")
