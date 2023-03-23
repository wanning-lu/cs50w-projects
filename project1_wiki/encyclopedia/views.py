from django.shortcuts import render
from django import forms
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from random import choice
from . import util
import markdown

from . import util

# Specify what type of form response we are getting
class SearchForm(forms.Form):
    form = forms.CharField()

class NewEntry(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea)

class EditEntry(forms.Form):
    content = forms.CharField(widget=forms.Textarea())

currentTitle = ""


# Home page of the wiki page
def index(request):
    # If the form sends information to the webpage
    if request.method == "POST":
        form = SearchForm(request.POST)

        if form.is_valid():
            # Retrieve the string of the response
            query = form.cleaned_data["form"]

            # If the exact string/query is found, redirect to its entry page
            if util.get_entry(query):
                return HttpResponseRedirect(f"wiki/{ query }")

            # Otherwise, search for similar entries containing the query as a substring 
            return HttpResponseRedirect(f"wiki/results/{ query }")

    # Render the homepage, which contains all of the wiki entries
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

# Bring up search results for a substring
def searchresults(request, query):
    matchingSubstring = []
    for entry in util.list_entries():
        if query in entry.lower():
                matchingSubstring.append(entry)

    return render(request, "encyclopedia/results.html", {
        "query": query,
        "entries": matchingSubstring,
        "form": SearchForm()
    })

# Return the corresponding entry for the URL
def gettitle(request, title):
    if util.get_entry(title):
        content = markdown.markdown(util.get_entry(title))
        return render(request, "encyclopedia/title.html", {
            "title": title,
            "content": content,
            "form": SearchForm(),
        })
    return HttpResponseNotFound("Entry not found!")

def new(request):
    if request.method == "POST":
        post = NewEntry(request.POST) 
        if post.is_valid():
            title = post.cleaned_data["title"]
            content = post.cleaned_data["content"]
            for entry in util.list_entries():
                if title == entry.lower():
                    return HttpResponseForbidden("Entry already exists!")
            util.save_entry(title, content)
            return HttpResponseRedirect(f"wiki/{ title }")

    return render(request, "encyclopedia/new.html", {
        "newEntry": NewEntry(),
    })

def edit(request, title):
    if request.method == "POST":
        content = EditEntry(request.POST)
        if content.is_valid():
            editedContent = content.cleaned_data["content"]
            util.save_entry(title, editedContent)
            return HttpResponseRedirect(f"../wiki/{ title }")
    return render(request, "encyclopedia/edit.html", {
        "editEntry": EditEntry(initial={'content': util.get_entry(title)}),
        "title": title
    })

def random(request):
    return HttpResponseRedirect(f"../../../wiki/{ choice(util.list_entries()) }")