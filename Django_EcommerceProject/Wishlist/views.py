from ast import Index
from email import message
from pyexpat.errors import messages
from django.shortcuts import render,redirect
from django.contrib import messages
from Admin.models import *
from.models import *
from UserSide.views import*
from django.shortcuts import get_object_or_404

# Create your views here.
def add_to_wishlist(request,id):
    wish=get_object_or_404(Products,id=id)
    Wishlist.objects.get_or_create(wished_product=wish,user=request.user)
    messages.success(request,'The item is added to your Wishlist')
    return redirect(index)


def ViewWishlist(request):
    user=request.user
    wishlist_list=Wishlist.objects.filter(user=user)
    return render(request,'Cart/wishlist.html',{'Wishlist_list':wishlist_list})

def remove_from_wishlist(request,id):
    user=request.user
    remove_item=Wishlist.objects.get(id=id)
    remove_item.delete()
    messages.error(request,'The item is removed from  your Wishlist')

    return redirect(ViewWishlist)
    

