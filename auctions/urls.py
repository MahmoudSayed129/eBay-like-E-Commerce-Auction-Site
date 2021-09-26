from django.urls import path

from . import views
from .models import Comments, active_list, WatchList, Bid 

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_auction", views.add_newlisting, name="add_auction"),
    path("view_listing", views.auction_view, name="auction_view"),
    path("closing", views.close, name="close"),
    path("adding_to_wathchlist", views.add_to_wathclist, name="add_to_wathclist"),
    path("removing_from_wathchlist", views.remove_from_wathclist, name="remove_from_wathclist"),
    path("Bid", views.place_bid, name="bid"),
    path("commenting", views.add_comment, name="commenting"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.category, name="category"),
    path("category/<str:category>", views.get_category, name="get_category")
]
