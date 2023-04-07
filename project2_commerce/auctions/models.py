from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid")
    price = models.DecimalField(max_digits=7, decimal_places=2)

class Listing(models.Model):
    CATEGORIES = [
        ("electronics", "Electronics"),
        ("clothing", "Clothing, Shoes, and Accessories"),
        ("sport", "Sporting Goods"),
        ("art", "Collectibles and Art"),
    ]
    name = models.CharField(max_length=128)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing")
    category = models.CharField(choices=CATEGORIES, max_length=64)
    desc = models.TextField()
    price = models.ForeignKey(Bid, on_delete=models.PROTECT, related_name="listing")
    imgurl = models.URLField()
    dateCreated = models.DateField(auto_now=False, auto_now_add=True)
    active = models.BooleanField(default=True)

    watchlistUsers = models.ManyToManyField(User, blank=True, related_name="watchlist")
    winner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="wonListing")

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    dateCreated = models.DateField(auto_now=False, auto_now_add=True)
