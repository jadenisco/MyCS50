from django.contrib.auth.models import AbstractUser
from django.db import models
from djmoney.models.fields import MoneyField


class Category(models.Model):
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"ID: {self.id}, Category: {self.description}"


class Comment(models.Model):
    comment = models.CharField(max_length=64)

    def __str__(self):
        return f"ID: {self.id}, Comment: {self.comment}"


class Bid(models.Model):
    amount = models.DecimalField(max_digits=10000, decimal_places=0)

    def __str__(self):
        return f"ID: {self.id}, Amount: {self.amount}"


class Listing(models.Model):
    description = models.CharField(max_length=100)
    comments  = models.ManyToManyField(Comment, blank=True,related_name="comments")
    bids = models.ManyToManyField(Bid, blank=True, related_name="comments")

    def __str__(self):
        return f"ID: {self.id}, Description: {self.description}"


class Auction(models.Model):
    listings = models.ManyToManyField(Listing, blank=True, related_name="listings")
    categories = models.ManyToManyField(Category, blank=True, related_name="categories")
    start_time = models.TimeField()
    duration = models.TimeField()
    def __str__(self):
        return f"ID: {self.id}, Listing: {self.listing}"


class User(AbstractUser):
    selling = models.ManyToManyField(Auction, blank=True, related_name="selling")
    buying = models.ManyToManyField(Auction, blank=True, related_name="buying")
