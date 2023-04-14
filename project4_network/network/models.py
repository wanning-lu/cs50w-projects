from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="followers")

class Post(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField("User", related_name="liked_posts", blank=True, null=True)

    
