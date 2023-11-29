from django.contrib.auth.models import AbstractUser
from django.db import models
from djmoney.models.fields import MoneyField


class Category(models.Model):
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.description}"


class Comment(models.Model):
    comment = models.CharField(max_length=64)

    def __str__(self):
        return f"ID: {self.id}, Comment: {self.comment}"


class Bid(models.Model):
    amount = models.DecimalField(max_digits=10000, decimal_places=0)

    def __str__(self):
        return f"ID: {self.id}, Amount: {self.amount}"


class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    image = models.URLField(blank=True)
    category = models.ManyToManyField(Category, blank=True, related_name="categories")
    comments  = models.ManyToManyField(Comment, blank=True,related_name="comments")

    def __str__(self):
        return f"ID: {self.id}, Title: {self.title}"


class Auction(models.Model):
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE, related_name="listing")
    bids = models.ManyToManyField(Bid, blank=True, related_name="bids")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"ID: {self.id} Listing: {self.listing.title}"


class User(AbstractUser):
    selling = models.ManyToManyField(Auction, blank=True, related_name="selling")
    buying = models.ManyToManyField(Auction, blank=True, related_name="buying")
