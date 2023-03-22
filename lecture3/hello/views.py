from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello, world!")

def wanning(request):
    return HttpResponse("heyyy girlie")

def greet(request, name):
    return HttpResponse(f"Hello, {name}!")

def html(request, name):
	return render(request, "hello/index.html", {
		"name": name.capitalize()
	})