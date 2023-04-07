from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.shortcuts import render
from django.urls import reverse
from .models import User, Bid, Listing, Comment
from django.core.exceptions import ValidationError

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
    imgurl = forms.URLField(label="Image URL (Optional)", required=False)

class CreateBid(forms.Form):
    newBid = forms.DecimalField(label="Bid", max_digits=7, decimal_places=2)

class CreateComment(forms.Form):
    comment = forms.CharField(label="Comment", widget=forms.Textarea)

def comment(request, listingnumber):
    inWatchlist = request.user.watchlist.filter(pk=listingnumber).first()
    listingItem = Listing.objects.get(pk=listingnumber)
    if inWatchlist == None:
        inWatchlist = False
    else:
        inWatchlist = True

    if request.method == "POST":
        form = CreateComment(request.POST)
        if form.is_valid():
            comment = form.cleaned_data["comment"]
            newComment = Comment(listing=listingItem, author=request.user, content=comment)
            newComment.save()
    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(pk=listingnumber),
        "inWatchlist": inWatchlist,
        "form": CreateBid(),
        "isBidder": request.user == listingItem.price.bidder,
        "isSeller": listingItem.seller == request.user,
        "comment": CreateComment(),
        "comments": listingItem.comments.all(),
        "active": listingItem.active,
    })


@login_required(redirect_field_name=None)
def watchlist(request):
    listings = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

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
            newListing = Listing(name=name, seller=request.user, desc=desc, 
                    price=startingBid, category=category, imgurl=imgurl)
            startingBid.save()
            newListing.save()
            return HttpResponseRedirect(reverse('index'))

    return render(request, "auctions/create.html", {
        "form": CreateListing()
    })

@login_required(redirect_field_name=None)
def listing(request, listingnumber):
    inWatchlist = request.user.watchlist.filter(pk=listingnumber).first()
    listingItem = Listing.objects.get(pk=listingnumber)
    if inWatchlist == None:
        inWatchlist = False
    else:
        inWatchlist = True

    if request.method == "POST":
        if inWatchlist:
            request.user.watchlist.remove(listingItem)
            inWatchlist = False
        else:
            request.user.watchlist.add(listingItem)
            inWatchlist = True

    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(pk=listingnumber),
        "inWatchlist": inWatchlist,
        "form": CreateBid(),
        "isBidder": request.user == listingItem.price.bidder,
        "isSeller": listingItem.seller == request.user,
        "comment": CreateComment(),
        "comments": listingItem.comments.all(),
        "active": listingItem.active,
    })

def bid(request, listingnumber):
    inWatchlist = request.user.watchlist.filter(pk=listingnumber).first()
    listingItem = Listing.objects.get(pk=listingnumber)
    if inWatchlist == None:
        inWatchlist = False
    else:
        inWatchlist = True

    if request.method == "POST":
        form = CreateBid(request.POST)

        if form.is_valid():
            bid = form.cleaned_data["newBid"]
            if (listingItem.seller == listingItem.price.bidder and bid >= listingItem.price.price) or (listingItem.seller != listingItem.price.bidder and bid > listingItem.price.price):
                newBid = Bid(bidder=request.user, price=bid)
                newBid.save()
                listingItem.price = newBid
                listingItem.save()
            else: 
                return render(request, "auctions/listing.html", {
                    "listing": Listing.objects.get(pk=listingnumber),
                    "inWatchlist": inWatchlist,
                    "form": CreateBid(),
                    "isBidder": request.user == listingItem.price.bidder,
                    "isSeller": listingItem.seller == request.user,
                    "active": listingItem.active,
                    "comment": CreateComment(),
                    "comments": listingItem.comments.all(),
                    "error": "Invalid bid!"
                })
        
    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(pk=listingnumber),
        "inWatchlist": inWatchlist,
        "form": CreateBid(),
        "isBidder": request.user == listingItem.price.bidder,
        "isSeller": listingItem.seller == request.user,
        "comment": CreateComment(),
        "comments": listingItem.comments.all(),
        "active": listingItem.active,
    })

def close(request, listingnumber):
    if request.method == "POST":
        listingItem = Listing.objects.get(pk=listingnumber)
        listingItem.winner = listingItem.price.bidder
        listingItem.active = False
        listingItem.save()
    return HttpResponseRedirect(reverse('index'))

def categoriesIndex(request):
    categoryModel = []
    for category in CATEGORIES:
        categoryModel.append(category[0])
        
    return render(request, "auctions/category-index.html", {
        "models": categoryModel,
    })

def categories(request, category):
    listings = Listing.objects.filter(category=category)
    return render(request, "auctions/category.html", {
        "listings": listings,
        "category": category
    })

def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings,
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
