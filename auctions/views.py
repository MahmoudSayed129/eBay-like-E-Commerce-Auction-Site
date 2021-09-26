from typing import List, final
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render
from django.urls import reverse

from .models import Comments, User,  active_list, Bid, WatchList

@login_required(login_url='login')
def index(request):
    a = active_list.objects.all()
    auctions = []
    for auction in a:
        if auction.closed_auction == False:
            auctions.append({"auction":auction})
    return render(request, "auctions/index.html", {"auctions":auctions})


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

@login_required(login_url='login')
def add_newlisting(request):
    if request.method == 'GET':
        return render (request, "auctions/add_auction.html")
    else:
        title = request.POST.get('title')
        img_url = request.POST.get('img')
        description = request.POST.get('description')
        bid = request.POST.get('bid')
        category = request.POST.get('category')
        if not bid or not title or not description :
            return render (request, "auctions/add_auction.html", {"error":True})
        if not img_url :
            img_url = "https://static.thenounproject.com/png/340719-200.png"
        if not category:
            category = "null" 
        auction = active_list.objects.create(
                user=request.user,
                title=title, 
                description=description, 
                final_bid=bid,
                category=category,
                img_url=img_url
            )
        return HttpResponseRedirect(reverse("index"))

@login_required(login_url='login')
def auction_view (requset):
    id = int(requset.POST.get('id'))
    auction = active_list.objects.get(pk = id)
    state = auction.closed_auction
    won = False
    if state:
        if Bid.objects.filter(auction_id=id).last():
            if Bid.objects.filter(auction_id=id).last().user == requset.user:
                won = True
    if auction.user== requset.user:
        owner = True
    else:
        owner = False
    watches = WatchList.objects.all()
    watched = False
    for watch in watches:
        if watch.auction_id == auction.id and watch.user == requset.user:
            watched = True
    c = Comments.objects.all()
    comments = []
    for comment in c:
        if comment.auction_id == auction.id:
            comments.append(comment)
    num_bids = Bid.objects.filter(auction_id=id).count()
    yours = False
    if Bid.objects.filter(auction_id=id).last():
        if auction.final_bid == Bid.objects.filter(auction_id=id).last().bid_amount:
            yours = True
    return render(requset, "auctions/auction.html", {"auction":auction, "won":won, "state":state, "owner":owner, "watched":watched, "comments":comments, "yours":yours, "num":num_bids})

@login_required(login_url='login')
def close(request):
    auction_id = request.POST.get('id')
    auction = active_list.objects.get(pk = auction_id)
    auction.closed_auction = True
    auction.save()
    return HttpResponseRedirect(reverse("index"))

@login_required(login_url='login')
def add_to_wathclist (request):
    auction_id = request.POST.get('id')
    auction = active_list.objects.get(pk = auction_id)
    new_watch = WatchList.objects.create(
        user=request.user,
        auction_id=auction_id
    )
    new_watch.auction_item.add(auction)
    if auction.user== request.user:
        owner = True
    else:
        owner = False
    c = Comments.objects.all()
    comments = []
    for comment in c:
        if comment.auction_id == auction.id:
            comments.append(comment)
    num_bids = Bid.objects.filter(auction_id=auction_id).count()
    yours = False
    if Bid.objects.filter(auction_id=auction_id).last():
        if auction.final_bid == Bid.objects.filter(auction_id=auction_id).last().bid_amount:
            yours = True
    return render(request, "auctions/auction.html", {"auction":auction, "owner":owner, "watched":True, "comments":comments, "yours":yours, "num":num_bids})

@login_required(login_url='login')   
def remove_from_wathclist(request):
    auction_id = int(request.POST.get('id'))
    auction = active_list.objects.get(pk = auction_id)
    watches = WatchList.objects.all()
    for watch in WatchList.objects.all():
        if watch.user == request.user and watch.auction_id == auction_id:
            WatchList.delete(watch)
    if auction.user== request.user:
        owner = True
    else:
        owner = False
    c = Comments.objects.all()
    comments = []
    for comment in c:
        if comment.auction_id == auction.id:
            comments.append(comment)
    num_bids = Bid.objects.filter(auction_id=auction_id).count()
    yours = False
    if Bid.objects.filter(auction_id=auction_id).last():
        if auction.final_bid == Bid.objects.filter(auction_id=auction_id).last().bid_amount:
            yours = True
    return render(request, "auctions/auction.html", {"auction":auction, "owner":owner, "watched":False, "comments":comments, "yours":yours, "num":num_bids})

@login_required(login_url='login')
def place_bid(request):
    auction_id = int(request.POST.get('id'))
    auction = active_list.objects.get(pk = auction_id)
    try:
        bid = int(request.POST.get('bid'))
    except:
        bid = 0
    final_bid = auction.final_bid
    if auction.user== request.user:
        owner = True
    else:
        owner = False
    watches = WatchList.objects.all()
    watched = False
    for watch in watches:
        if watch.auction_id == auction.id and watch.user == request.user:
            watched = True
    c = Comments.objects.all()
    comments = []
    for comment in c:
        if comment.auction_id == auction.id:
            comments.append(comment)
    num_bids = Bid.objects.filter(auction_id=auction_id).count()
    yours = False
    if Bid.objects.filter(auction_id=auction_id).last():
        if auction.final_bid == Bid.objects.filter(auction_id=auction_id).last().bid_amount:
            yours = True
    if bid <= final_bid:
        return render(request, "auctions/auction.html", {"auction":auction, "owner":owner, "watched":watched, "comments":comments, "biderror":True, "yours":yours, "num":num_bids})
    else:
        auction.final_bid = bid
        auction.save()
        new_bid = Bid.objects.create(
            user =request.user,
            bid_amount = bid,
            auction_id=auction_id
            )
        new_bid.auction_item.add(auction)
        num_bids = Bid.objects.filter(auction_id=auction_id).count()
        return render(request, "auctions/auction.html", {"auction":auction, "owner":owner, "watched":False, "comments":comments, "yours":True, "num":num_bids})

@login_required(login_url='login')
def add_comment(request):
    auction_id = int(request.POST.get('id'))
    auction = active_list.objects.get(pk = auction_id)
    commente = request.POST.get('comment')
    watches = WatchList.objects.all()
    watched = False
    for watch in watches:
        if watch.auction_id == auction.id and watch.user == request.user:
            watched = True
    if auction.user== request.user:
        owner = True
    else:
        owner = False
    num_bids = Bid.objects.filter(auction_id=auction_id).count()
    yours = False
    if Bid.objects.filter(auction_id=auction_id).last():
        if auction.final_bid == Bid.objects.filter(auction_id=auction_id).last().bid_amount:
            yours = True
    c = Comments.objects.all()
    comments = []
    for comment in c:
        if comment.auction_id == auction.id:
            comments.append(comment)
    if not commente:
        return render(request, "auctions/auction.html", {"auction":auction, "owner":owner, "watched":watched, "comments":comments, "commenterror":True, "yours":yours, "num":num_bids})
    else:
        new_comment = Comments.objects.create(
            user=request.user,
            comment=commente,
            auction_id=auction_id
        )
        new_comment.auction_item.add(auction)
        c = Comments.objects.all()
        comments = []
        for comment in c:
            if comment.auction_id == auction.id:
                comments.append(comment)
        return render(request, "auctions/auction.html", {"auction":auction, "owner":owner, "watched":False, "comments":comments, "yours":yours, "num":num_bids})

@login_required(login_url='login')
def watchlist(request):
    w = WatchList.objects.all()
    auctions = []
    for watch in w:
        if watch.user==request.user:
            auctions.append({"auction":active_list.objects.get(pk=watch.auction_id), "state":active_list.objects.get(pk=watch.auction_id).closed_auction})
    return render(request, "auctions/index.html", {"auctions":auctions, "watchlist":True})

@login_required(login_url='login')
def category(request):
    categories=[]
    auctions = active_list.objects.all()
    for auction in auctions:
        if auction.category not in categories and not auction.category == "null":
            categories.append(auction.category)
    return render(request, "auctions/categories.html", {"categories":categories})

@login_required(login_url='login')
def get_category(request, category):
    listings = active_list.objects.all()
    auctions = []
    for listing in listings:
        if listing.category == category:
            auctions.append({"auction":listing, "state":listing.closed_auction})
    return render(request, "auctions/index.html", {"auctions":auctions})
