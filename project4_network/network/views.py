from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import User, Post

class NewPost(forms.Form):
    content = forms.CharField(label="", widget=forms.Textarea)


def index(request):
    if request.method == "POST":
        form = NewPost(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            post = Post(author=request.user, content=content)
            post.save()

    return render(request, "network/index.html", {
        "form": NewPost(),
        "posts": Post.objects.all().order_by("-timestamp").all()
    })

@csrf_exempt
@login_required
def following(request, userId):

    # Update user's following list
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("following") is not None:
            user.following.add = data["following"]
        email.save()
        return HttpResponse(status=204)

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)

def users(request, userId):
    user = User.objects.get(pk=userId)
    return render(request, "network/user.html", {
        "userProfile": user,
        "posts": user.posts.all().order_by("-timestamp").all(),
        "followers": user.followers.all()
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
