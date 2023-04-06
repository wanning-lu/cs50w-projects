from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.shortcuts import render
from django.urls import reverse
from .models import User, Bid, Listing, Comment

CATEGORIES = [
    ("electronics", "Electronics"),
    ("clothing", "Clothing, Shoes, and Accessories"),
    ("sport", "Sporting Goods"),
    ("art", "Collectibles and Art"),
]

class CreateListing(forms.Form):
    name = forms.CharField(label="Item")
    desc = forms.CharField(label="Description", widget=forms.Textarea)
    price = forms.DecimalField(label="Starting bid", max_digits=7, decimal_places=2)
    category = forms.ChoiceField(choices=CATEGORIES)
    imgurl = forms.URLField(label="Image URL (Optional)")

@login_required(redirect_field_name=None)
def watchlist(request):
    pass

@login_required(redirect_field_name=None)
def create(request):
    if request.method == "POST":
        form = CreateListing(request.POST)

        if form.is_valid():
            # Retrieve data
            name = form.cleaned_data["name"]
            desc = form.cleaned_data["desc"]
            price = form.cleaned_data["price"]
            category = form.cleaned_data["category"]
            imgurl = form.cleaned_data["imgurl"]

            startingBid = Bid(bidder=request.user, price=price)
            newListing = Listing(name=name, seller=request.user, desc=desc, price=startingBid, category=category, imgurl=imgurl)
            startingBid.save()
            newListing.save()
            return HttpResponseRedirect(reverse('index'))

    return render(request, "auctions/create.html", {
        "form": CreateListing()
    })

def listing(request, listingnumber):
    inWatchlist = request.user.watchlist.filter(pk=listingnumber).first()
    if inWatchlist == None:
        inWatchlist = False
    else:
        inWatchlist = True

    if request.method == "POST":
        listingItem = Listing.objects.get(pk=listingnumber)
        if inWatchlist:
            request.user.watchlist.remove(listingItem)
            inWatchlist = False
        else:
            request.user.watchlist.add(listingItem)
            inWatchlist = True

        return render(request, "auctions/listing.html", {
            "listing": Listing.objects.get(pk=listingnumber),
            "inWatchlist": inWatchlist
        })

    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(pk=listingnumber),
        "inWatchlist": inWatchlist
    })

def categories(request):
    pass

def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
