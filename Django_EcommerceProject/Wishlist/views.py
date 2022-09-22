from django.shortcuts import render,redirect
from django.contrib import messages
from Admin.models import *
from.models import *
from UserSide.views import*
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='Index')
def add_to_wishlist(request,id):
    wish=get_object_or_404(Products,id=id)
    Wishlist.objects.get_or_create(wished_product=wish,user=request.user)
    messages.success(request,'The item is added to your Wishlist')
    return redirect(index)

@login_required(login_url='Index')
def ViewWishlist(request):
    user=request.user
    wishlist_list=Wishlist.objects.filter(user=user)
    return render(request,'Cart/wishlist.html',{'Wishlist_list':wishlist_list})

@login_required(login_url='Index')
def remove_from_wishlist(request,id):
    if request.method=='POST':
        user=request.user
        remove_item=Wishlist.objects.get(id=id,user=user)
        remove_item.delete()
        # messages.error(request,'The item is removed from  your Wishlist')

        return redirect(ViewWishlist)
    

