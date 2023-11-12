from django.contrib.auth.models import AbstractUser
from django.db import models

class Profile(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField()

    def __str__(self):
        return f"ID: {self.id}, Name: {self.first_name} {self.last_name} Email: {self.email}"

class Auction(models.Model):
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="seller")
    time_created = models.IntegerField()
    duration = models.IntegerField()

    def __str__(self):
        return f"ID: {self.id}, Seller: {self.seller}"

class Listing(models.Model):
    description = models.CharField(max_length=64)
    price = models.IntegerField()
    created = models.IntegerField()
    auctions = models.ManyToManyField(Auction, blank=True, related_name="listings")

    def __str__(self):
        return f"ID: {self.id}, Description: {self.description}"

class Bid(models.Model):
    price = models.IntegerField()

    def __str__(self):
        return f"ID: {self.id}, Price: {self.price}"
class Comment(models.Model):
    comment = models.CharField(max_length=64)

    def __str__(self):
        return f"ID: {self.id}, Comment: {self.comment}"


'''
class User(AbstractUser):
    pass
'''
