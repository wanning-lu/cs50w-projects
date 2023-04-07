from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categoriesIndex, name="categoriesIndex"),
    path("categories/<str:category>", views.categories, name="categories"),
    path("create", views.create, name="create"),
    path("listings/<int:listingnumber>", views.listing, name="listing"),
    path("bid/<int:listingnumber>", views.bid, name="bid"),
    path("close/<int:listingnumber>", views.close, name="close"),
    path("comment/<int:listingnumber>", views.comment, name="comment")
]
