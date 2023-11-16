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

class Listing(models.Model):
    description = models.CharField(max_length=64)
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="bids")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return f"ID: {self.id}, Description: {self.description}, Comment: {self.comment} Bid: {self.bid}"

class Auction(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listings")

    def __str__(self):
        return f"ID: {self.id}, Listing: {self.listing}"

class Profile(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField()
    auctions = models.ManyToManyField(Auction, blank=True, related_name="auctions")

    def __str__(self):
        return f"ID: {self.id}, Name: {self.first_name} {self.last_name} Email: {self.email} Auctions: {self.auctions}"
