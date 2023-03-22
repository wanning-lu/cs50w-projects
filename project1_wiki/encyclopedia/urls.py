from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.gettitle, name="gettitle"),
    path("wiki/results/<str:query>", views.searchresults, name="searchresults"),
    path("new", views.new, name="newentry"),
    path("edit/<str:title>", views.edit, name="editentry")
]
