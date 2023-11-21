from django.contrib.auth.models import AbstractUser
from django.db import models

class Comment(models.Model):
    comment = models.CharField(max_length=64)

    def __str__(self):
        return f"ID: {self.id}, Comment: {self.comment}"

class Bid(models.Model):
    amount = models.IntegerField()

    def __str__(self):
        return f"ID: {self.id}, Amount: {self.amount}"

class Auction(models.Model):
    description = models.CharField(max_length=64)

    def __str__(self):
        return f"ID: {self.id}, Listing: {self.listing}"

class Listing(models.Model):
    description = models.CharField(max_length=64)

    def __str__(self):
        return f"ID: {self.id}, Description: {self.description}"

class User(AbstractUser):
    listings = models.ManyToManyField(Listing, blank=True, related_name="users")
