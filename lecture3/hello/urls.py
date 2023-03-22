from django.urls import path
from . import views

urlpatterns = [
    # name makes it easy to reference it
    path("", views.index, name="index"),
    path("html<str:name>", views.html, name="html"),
    path("<str:name>", views.greet, name="greet"),
    
]