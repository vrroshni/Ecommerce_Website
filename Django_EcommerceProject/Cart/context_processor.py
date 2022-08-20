from Admin.models import *
from Accounts.models import *
from .models import *
from.views import *





def count(request):
    products_count=0;
    if 'admin' in request.path:
        return{}
    else:
        try:
            cartitems_id=Cart.objects.filter(cart_id=create_cart_id(request))
            cart_items=Cart_Products.objects.all().filter(cart=cartitems_id[:1])
            for no_cartitems in cart_items:
                products_count+=no_cartitems.quantity
        except Cart.DoesNotExist:
            products_count=0
        return dict(Products_count=products_count)
