from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("User", related_name="user_follows")
    followers = models.ManyToManyField("User", related_name="user_following")


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    timestamp = models.DateTimeField(auto_now_add=True)
    body = models.TextField(blank=True)
    likes = models.ManyToManyField("User", related_name="user_like")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.user.username,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "body": self.body,
            "likes": [l.username for l in self.likes.all()]
        }