from django.contrib.auth.models import AbstractUser
from django.db import models

class Auction(models.Model):
    name = models.CharField(max_length=64) 
    price = models.CharField(max_length=64)
    created = models.IntegerField()    

class User(AbstractUser):
    pass
