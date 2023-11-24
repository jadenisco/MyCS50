from django.contrib.auth.models import AbstractUser
from django.db import models
from djmoney.models.fields import MoneyField

class Comment(models.Model):
    comment = models.CharField(max_length=64)

    def __str__(self):
        return f"ID: {self.id}, Comment: {self.comment}"

class Bid(models.Model):
    bid = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')

    def __str__(self):
        return f"ID: {self.id}, Amount: {self.bid}"

class Auction(models.Model):
    description = models.CharField(max_length=64)

    def __str__(self):
        return f"ID: {self.id}, Listing: {self.listing}"

class Listing(models.Model):
    description = models.CharField(max_length=100)
    comments  = models.CharField(max_length=10000)
    initial_bid = models.DecimalField(max_digits=10000, decimal_places=0)

    def __str__(self):
        return f"ID: {self.id}, Description: {self.description}"

class User(AbstractUser):
    listings = models.ManyToManyField(Listing, blank=True, related_name="users")
