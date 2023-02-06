from telnetlib import STATUS
from urllib import request
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from pkg_resources import require

from .models import  User, Category,Listing,Comment,Bid


def index(request):
    active=Listing.objects.filter(status=True)
    categoryall=Category.objects.all()
    return render(request, "auctions/index.html",{
      "listing":active,
      "categories": categoryall
    })
        

    
def newBid(request,id):
    nbid=request.POST['nbid']
    lista=Listing.objects.get(pk=id)
    add= request.user in lista.listUser.all()
    userbid= request.user.username == lista.seller.username
    comments= Comment.objects.filter(listing=lista)
    categoryall=Category.objects.all()

    if int(nbid) > lista.price.bid:
        newBid= Bid(user=request.user, bid=int(nbid))
        newBid.save()
        lista.price=newBid
        lista.save()
        return render(request,"auctions/listingProduct.html", {
            "categoryall":categoryall,
            "listing":lista,
            'add':add,
            'userbid':userbid,
            'comments':comments,
            "update":True,
            "message": "New Bid introduce"
            
            
        })
    else:
        return render(request,"auctions/listingProduct.html", {
            "listing":lista,
                        'add':add,

            "message": "New Bid introduce Fail",
            "update":False,
           "categoryall":categoryall
            
         }) 



def listingProduct(request,id):
    lista = Listing.objects.get(pk =id)
    active=Listing.objects.filter(status=True)
    add= request.user in lista.listUser.all()
    comments= Comment.objects.filter(listing=lista)
    userbid= request.user.username == lista.seller.username
    viewsCategory=Category.objects.all()

  
   
    
    

    return render(request,"auctions/listingProduct.html",{
    'listing': lista,
    'status':active,
    'comments':comments,
    'add': add,
    'userbid':userbid,
    "categories":viewsCategory
    
    


    })

def close(request, id):
        lista = Listing.objects.get(pk =id)
        lista.status=False
        lista.save()
        add= request.user in lista.listUser.all()
        userbid= request.user.username == lista.seller.username
        


        return render (request,"auctions/listingProduct.html",{
              'listing': lista,
              'add':add,
              'userbid':userbid,
              'update':True,
              'message': "Auction close"




        })
   
    
def addWatch(request,id):
    lista=Listing.objects.get(pk =id)
    usert=request.user
    lista.listUser.add(usert)
    return HttpResponseRedirect(reverse("listingProduct", args=(id, )))
 
def remove(request,id):
    lista=Listing.objects.get(pk =id)
    usert=request.user
    lista.listUser.remove(usert)
    return HttpResponseRedirect(reverse("listingProduct", args=(id, )))

def viewlisting(request):
    user=request.user
    active=user.listUser.all()
    viewsCategory=Category.objects.all()

    return render(request,"auctions/viewlistin.html", {
        "view":active,
        "categories":viewsCategory
    })

    

def listCategory (request):
    if request.method=="POST":
        categoryList=request.POST['category']
        category=Category.objects.get(name=categoryList)
        active=Listing.objects.filter(status=True, category=category)
        categoryall=Category.objects.all()
        return render(request, "auctions/index.html",{
         "listing":active,
         "categories": categoryall,

    })

    
def categories (request):
    if request.method=="POST":
        categoryList=request.POST['category']
        category=Category.objects.get(name=categoryList)
        active=Listing.objects.filter(status=True, category=category)
        categoryall=Category.objects.all()
        return render(request, "auctions/index.html",{
         "listing":active,
         "categories": categoryall

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
      if request.method =="GET":
        viewsCategory=Category.objects.all()
        return render (request, "auctions/register.html",{
            "categories":viewsCategory,
            
        })
  

      elif request.method == "POST":
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


def create(request):
    
    if request.method =="GET":
        viewsCategory=Category.objects.all()
        return render (request, "auctions/create.html",{
            "categories":viewsCategory,
            
        })
    else:
        title = request.POST["title"]
        description=request.POST["description"]
        image=request.POST["image"]
      
        price=request.POST["price"]
        category=request.POST["category"]
        seller=request.user
        categoryall=Category.objects.get(name=category)
        bid = Bid(bid=int(price), user=seller)
        bid.save()

        createListing= Listing(
            title=title,
            description=description,
            image=image,
           
            price=bid,
            category=categoryall,
            seller=seller

    )
    createListing.save()
    return HttpResponseRedirect(reverse("index"))
 
def comments(request,id):
    user= request.user
    listing=Listing.objects.get(pk=id)
    comment= request.POST['newComment']
    
    newComment=Comment(
    user=user,
    listing=listing,
    comment=comment
 )
    newComment.save()
    return HttpResponseRedirect(reverse("listingProduct", args=(id, )))



     