
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listCategory", views.listCategory, name="listCategory"),
    path("listCategory", views.categories, name="categories"),
    path("auctions/<int:id>",views.listingProduct, name="listingProduct"),
    path("addWatch/<int:id>",views.addWatch,name="addWatch"),
    path("remove/<int:id>",views.remove,name="remove"),
    path("viewlisting",views.viewlisting, name="viewlisting"),
    path("comments/<int:id>",views.comments,name="comments"),
    path("newBid/<int:id>",views.newBid,name="newBid"),
    path("close/<int:id>",views.close,name="close"),

    
 

   

]
