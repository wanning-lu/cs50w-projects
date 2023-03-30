from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid")
    price = models.DecimalField(max_digits=7, decimal_places=2)

class Listing(models.Model):
    name = models.CharField(max_length=128)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing")
    category = models.CharField(max_length=64)
    desc = models.TextField()
    price = models.ForeignKey(Bid, on_delete=models.PROTECT, related_name="listing")
    imgurl = models.URLField()


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
