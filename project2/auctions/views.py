
from itertools import count
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Max ,Count
from .models import User,Listing,Bidding,Category,Comment,Image, Wishlist
from datetime import datetime


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html",{
        'listings': listings
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
    
@login_required
def new_listing(request):
    if request.method == 'GET':
        return render(request, "auctions/new_listing.html")
    else:
        listing_title = request.POST.get('listing_title')
        if listing_title == "":
            messages.add_message(request,messages.WARNING,"Title cannot be blank")
            return HttpResponseRedirect(reverse("new_listing"))
        listing_description = request.POST.get('listing_description')
        if listing_description == "":
            messages.add_message(request,messages.WARNING,"Description cannot be blank")
            return HttpResponseRedirect(reverse("new_listing"))
        starting_bid = request.POST.get('starting_bid')
        if starting_bid =="":
            messages.add_message(request,messages.WARNING,"Starting bid cannot be blank")
            return HttpResponseRedirect(reverse("new_listing"))
        listing_image = request.POST.get('listing_image')
        listing_category = request.POST.get('listing_category')
        if listing_category == "":
            messages.add_message(request,messages.WARNING,"Category cannot be blank")
            return HttpResponseRedirect(reverse("new_listing"))
        reserve_price = request.POST.get('reserve_price')
        if reserve_price == "":
            messages.add_message(request,messages.WARNING,"Reserve price cannot be blank")
            return HttpResponseRedirect(reverse("new_listing"))
        end_date = request.POST.get('end_time')
        if end_date == "":
            messages.add_message(request,messages.WARNING,"End date cannot be blank")
            return HttpResponseRedirect(reverse("new_listing"))
        check_category = Category.objects.filter(name=listing_category).first()
        if check_category:
            new_listing = Listing.objects.create(title=listing_title, seller=request.user,description=listing_description,starting_bid=starting_bid,current_bid=starting_bid,reserve_price=reserve_price,end_time=end_date,category=check_category)
            new_listing.save()
        else:
            new_category = Category.objects.create(name=listing_category)
            new_category.save()
            new_listing = Listing.objects.create(title=listing_title, seller=request.user,description=listing_description,starting_bid=starting_bid,current_bid=starting_bid,reserve_price=reserve_price,end_time=end_date,category=new_category)
            new_listing.save()
            
        new_image = Image.objects.create(image_url=listing_image,listing=new_listing)
        new_image.save()
        messages.add_message(request,messages.SUCCESS,"Listing Created Successfully")
        return HttpResponseRedirect(reverse("index"))
    
    
@login_required
def listing_page(request,listing_id):
    if request.method == 'GET': 
        user = request.user
        listing = get_object_or_404(Listing,pk=listing_id)
        image = listing.listing_image.all()
        images = image.first().image_url
        items = Wishlist.objects.filter(user=user,listing=listing)
        wish_item = [item.listing for item in items]
        return render(request,"auctions/listing_page.html",{
            "listings":listing,
            "image":images,
            "items":wish_item
        })
    else:
        listing = get_object_or_404(Listing,pk=listing_id)
        bid_amount = request.POST.get('bid_amount')
        try:
            bid_amount = float(bid_amount)
        except ValueError:
            messages.add_message(request,messages.WARNING,'Invalid Amount Please enter a correct format')
            return HttpResponseRedirect(reverse('listing_page',args=[listing.id]))
        if bid_amount <= listing.current_bid:
            messages.add_message(request,messages.WARNING,'Bidding amount must be greater than current highest bid')
            return HttpResponseRedirect(reverse('listing_page',args=[listing.id]))
        user = request.user
        bid = Bidding.objects.create(listing=listing,user=user,bid_amount=bid_amount)
        bid.save()
        listing.current_bid = bid_amount
        listing.save()
        messages.add_message(request,messages.SUCCESS,'Bid placed Successfully')
        return HttpResponseRedirect(reverse('listing_page',args=[listing.id]))

@login_required
def comment(request,listing_id):
    if request.method == 'POST':
        listing = get_object_or_404(Listing,pk=listing_id)
        user = request.user
        comment = request.POST.get('comment')
        if comment == "":
            messages.add_message(request,messages.WARNING,"Can't send an empty request")
            return HttpResponseRedirect(reverse('listing_page',args=[listing.id]))
        new_comment = Comment.objects.create(text=comment,user=user,listing=listing)
        new_comment.save()
        messages.add_message(request,messages.SUCCESS,'comment uploaded')
        return HttpResponseRedirect(reverse('listing_page',args=[listing.id]))
        
@login_required
def add_to_wishlist(request,listing_id):
    if request.method == 'POST':
        user = request.user
        listing = get_object_or_404(Listing,pk=listing_id)
        wish_item = request.POST.get('wish')
        if wish_item == "Add":
            wish = Wishlist.objects.create(user=user,listing=listing)
            wish.save()
            messages.add_message(request,messages.SUCCESS,"Added item to wishlist")
        else:
            wish = Wishlist.objects.filter(user=user,listing=listing).delete()
            messages.add_message(request,messages.SUCCESS,"Removed item from wishlist")
        return HttpResponseRedirect(reverse('listing_page',args=[listing.id]))
        
@login_required
def close_listing(request,listing_id):
    if request.method == 'POST':
        listing = get_object_or_404(Listing,pk=listing_id)
        if request.user == listing.seller:
            listing.closed = True
            highest_bid = listing.current_bid
            bidding = Bidding.objects.filter(bid_amount=highest_bid,listing=listing)
            for bid in bidding:
                listing.winner = bid.user
            listing.save()
        else:
            messages.add_message(request,messages.WARNING,"You are not the seller of this listing")
             
        return HttpResponseRedirect(reverse('listing_page',args=[listing.id]))
        
        
        
        
@login_required
def wish_list_page(request):
    user = request.user
    items = Wishlist.objects.filter(user=user)
    wish_item = [item.listing for item in items]
    return render(request,"auctions/wishlist.html",{
        "items":wish_item
    })


@login_required
def view_categories(request):
    categories = Category.objects.all()
    return render(request,"auctions/category.html",{
        "categories":categories
    })
    
@login_required
def display_category(request,category_id):
    category = get_object_or_404(Category,pk=category_id)
    listings_in_category = category.listings.all()
    return render(request,"auctions/display.html",{
        "listings":listings_in_category,
        "category":category
    })