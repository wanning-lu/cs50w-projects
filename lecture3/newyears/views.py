from django.shortcuts import render
import datetime

# Create your views here.

def index(request):
    now = datetime.datetime.now()
    isitnewyears = "NO"
    if now.month == 1 and now.day == 1:
        isitnewyears = "NO"
    return render(request, "newyears/index.html", {
            "isitnewyears": isitnewyears
        })
