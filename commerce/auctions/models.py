
from unittest.util import _MAX_LENGTH
from urllib import request
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass

class Category(models.Model):
    name= models.CharField(max_length=64)
    
    def __str__(self):
        return f"{self.name}"




class Bid(models.Model):
 user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="uBid")
 bid=models.IntegerField()
   



class Listing(models.Model):
    title=models.CharField(max_length=64)
    description=models.CharField(max_length=500)
    image=models.CharField(max_length=1000)
    startingPrice=models.IntegerField(default=0)
    price= models.ForeignKey(Bid,on_delete=models.CASCADE,blank=True,null=True,related_name="listingBid")
    status=models.BooleanField(default=True)
    seller=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="user")
    category=models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True,related_name="category")
    listUser = models.ManyToManyField(User, blank = True,  null = True, related_name ="listUser")
    date = models.DateTimeField(default=timezone.now)
    
class Comment(models.Model):
        comment = models.TextField(max_length=500)
        user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="uComment")
        listing = models.ForeignKey( Listing ,on_delete=models.CASCADE,blank=True,null=True,related_name="lComment")
        date = models.DateTimeField(default=timezone.now)
        def __str__(self):
          return f"{self.user} {self.listing}"

