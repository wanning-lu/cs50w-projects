from django.shortcuts import render
from django import forms
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
import markdown

from . import util

class NewTaskForm(forms.Form):
    form = forms.CharField()

def index(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["form"]
            if util.get_entry(query):
                return HttpResponseRedirect(f"wiki/{ query }")
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewTaskForm()
    })

def gettitle(request, title):
    if util.get_entry(title):
        content = markdown.markdown(util.get_entry(title))
        return render(request, "encyclopedia/title.html", {
            "title": title,
            "content": content
        })
    return HttpResponseNotFound("Entry not found!")

    



