from django.shortcuts import render,redirect,get_object_or_404
from Admin.models import*
from Accounts.models import*
from Cart.models import*
from Order.models import*
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from UserSide.views import *
from datetime import date
from django.http import JsonResponse
import json


# Create your views here.





# ----------------- creating separate sessions for each user----------------- #
def create_cart_id(request):
    cart_id=request.session.session_key
    if not  cart_id:
        cart_id=request.session.create()
    return cart_id




# ---------------------- funtionality for adding to cart --------------------- #
#add to cart from index page
def add_ToCart(request,id):
    #product is adding with its id 
    product=Products.objects.get(id=id)
    #if there is chance to have error
    if request.user.is_authenticated:
        try:
            cart__id=Cart.objects.get(cart_id=create_cart_id(request))#took sessionkeyif it is exists
        except Cart.DoesNotExist:
            cart__id=Cart.objects.create(cart_id=create_cart_id(request))#created sessionkey if it doesnot exists  
            cart__id.save()
        # to take objects from Cart_Products
        try:
            cart_items=Cart_Products.objects.get(product=product,cart=cart__id,user=request.user)
            if cart_items.quantity<cart_items.product.stock:#checking quantity with stock
                cart_items.quantity+=1#increasing the quantity 
                messages.success(request,'Your Product is Added to Your cart')
                cart_items.save()
            else:
                messages.error(request,'Stock Not Available')
        except Cart_Products.DoesNotExist:#not available,create one
            cart_items=Cart_Products(product=product,cart=cart__id,user=request.user)
            if cart_items.product.stock >0:#checking quantity with stock
                cart_items.quantity=1#increasing the quantity 
                messages.success(request,'Your Product is Added to Your cart')
                cart_items.save()
            else:
                messages.error(request,'Stock Not Available')

    
    else:
        try:
            cart__id=Cart.objects.get(cart_id=create_cart_id(request))#took sessionkeyif it is exists
        except Cart.DoesNotExist:
            cart__id=Cart.objects.create(cart_id=create_cart_id(request))#created sessionkey if it doesnot exists  
            cart__id.save()
        # to take objects from Cart_Products
        try:
            cart_items=Cart_Products.objects.get(product=product,cart=cart__id)
            if cart_items.quantity<cart_items.product.stock:#checking quantity with stock
                cart_items.quantity+=1#increasing the quantity 
                messages.success(request,'Your Product is Added to Your cart')
                cart_items.save()
            else:
                messages.error(request,'Stock Not Available')
        except Cart_Products.DoesNotExist:#not available,create one
            cart_items=Cart_Products(product=product,cart=cart__id)
            if cart_items.product.stock >0:#checking quantity with stock
                cart_items.quantity=1#increasing the quantity 
                messages.success(request,'Your Product is Added to Your cart')
                cart_items.save()
            else:
                messages.error(request,'Stock Not Available')
    return redirect('Index')



#------------------------ list the items in the cart ------------------------ #

def view_cart(request,total=0,count=0,cartlist_items=None,rawtotal=0):
    request.session['wallet']=None
    request.session['coupon']=None
    request.session['amountfromwallet']=None
    request.session['before_coupon_amount']=None

    try:
        if request.user.is_authenticated:
            cartlist_items=Cart_Products.objects.filter(is_active=True,user=request.user).order_by('id')
            for i in cartlist_items:
                        if i.product.discount_price>0:
                            total+=(i.product.discount_price*i.quantity)
                            count+=i.quantity
                        else:
                            total+=(i.product.price*i.quantity)
                            count+=i.quantity
                        rawtotal+=(i.product.price*i.quantity)    
        else:
            cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
            cartlist_items=Cart_Products.objects.filter(cart=cart_itemsid,is_active=True)
            for i in cartlist_items:
                        if i.product.discount_price>0:
                            total+=(i.product.discount_price*i.quantity)
                            count+=i.quantity
                        else:
                            total+=(i.product.price*i.quantity)
                            count+=i.quantity
                        rawtotal+=(i.product.price*i.quantity)
    except ObjectDoesNotExist:
           pass
    request.session['original amount']=total
    subtotal=total
    tax = (2 * subtotal)/100
    alltotal=int(tax+subtotal)#after having tax
    request.session['Totalamount']=int(alltotal)
    context={
        'Cart_items':cartlist_items,
        'Total':alltotal,
        'Count':count,
        'Tax':tax,
        'Subtotal':subtotal,
        'WithOutDiscount':rawtotal
    }
    return render(request,'Cart/ViewCart.html',context)




# ----------------------- decrease the quantity in cart ---------------------- #
def decrease_quantity_cart(request,id):
    total=0
    count=0
    cartlist_items=None
    rawtotal=0
    try:
        if request.user.is_authenticated:
            product=get_object_or_404(Products,id=id)#this will find the object from mentioned model ,in a given certain conditions
            cartlist_items=Cart_Products.objects.filter(is_active=True,user=request.user)
            for i in cartlist_items:
                        if i.product.discount_price>0:
                            total+=(i.product.discount_price*i.quantity)
                            count+=i.quantity
                        else:
                            total+=(i.product.price*i.quantity)
                            count+=i.quantity
                        rawtotal+=(i.product.price*i.quantity) 
            cart_items=Cart_Products.objects.get(product=product,user=request.user)
            if cart_items.quantity>1:
                cart_items.quantity-=1
                cart_items.save()
            else:
                pass
        else:
            cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
            product=get_object_or_404(Products,id=id)#this will find the object from mentioned model ,in a given certain conditions
            cartlist_items=Cart_Products.objects.filter(cart=cart_itemsid,is_active=True)
            for i in cartlist_items:
                        if i.product.discount_price>0:
                            total+=(i.product.discount_price*i.quantity)
                            count+=i.quantity
                        else:
                            total+=(i.product.price*i.quantity)
                            count+=i.quantity
                        rawtotal+=(i.product.price*i.quantity) 
            cart_items=Cart_Products.objects.get(product=product,cart=cart_itemsid)
            if cart_items.quantity>1:
                cart_items.quantity-=1
                cart_items.save()
            else:
                pass

    except ObjectDoesNotExist:
           pass
    print(rawtotal)#without discount    
    subtotal=total
    print('after discount')
    print(subtotal)#with discount
    tax = (2 * subtotal)/100
    alltotal=tax+subtotal#after having tax
    context={
        'Cart_items':cartlist_items,
        'Total':alltotal,
        'Count':count,
        'Tax':tax,
        'Subtotal':subtotal,
        'WithOutDiscount':rawtotal,
    }
    return render(request,'Cart/htmx-cart.html',context)


# ----------------------- increase the quantity in cart ---------------------- #
def increase_quantity_cart(request,id):
    total=0
    count=0
    cartlist_items=None
    rawtotal=0
    try:
        if request.user.is_authenticated:
            product=get_object_or_404(Products,id=id)#this will find the object from mentioned model ,in a given certain conditions
            cartlist_items=Cart_Products.objects.filter(is_active=True,user=request.user)
            for i in cartlist_items:
                        if i.product.discount_price>0:
                            total+=(i.product.discount_price*i.quantity)
                            count+=i.quantity
                        else:
                            total+=(i.product.price*i.quantity)
                            count+=i.quantity
                        rawtotal+=(i.product.price*i.quantity)
            cart_items=Cart_Products.objects.get(product=product,user=request.user)
            if cart_items.quantity>=1 :
                if cart_items.quantity<cart_items.product.stock:#checking quantity with stock
                    cart_items.quantity+=1#increasing the quantity 
                    cart_items.save()
                else:
                    messages.error(request,'Stock Not Available')
            else:
                    pass
        else:
            cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
            product=get_object_or_404(Products,id=id)#this will find the object from mentioned model ,in a given certain conditions
            cartlist_items=Cart_Products.objects.filter(cart=cart_itemsid,is_active=True)
            for i in cartlist_items:
                        if i.product.discount_price>0:
                            total+=(i.product.discount_price*i.quantity)
                            count+=i.quantity
                        else:
                            total+=(i.product.price*i.quantity)
                            count+=i.quantity
                        rawtotal+=(i.product.price*i.quantity)
            cart_items=Cart_Products.objects.get(product=product,cart=cart_itemsid)
            if cart_items.quantity>=1:
                if cart_items.quantity<cart_items.product.stock:#checking quantity with stock
                    cart_items.quantity+=1#increasing the quantity 
                    cart_items.save()
                else:
                    messages.error(request,'Stock Not Available')
            else:
                    pass
    except ObjectDoesNotExist:
           pass
    print(rawtotal)#without discount    
    subtotal=total
    print('after discount')
    print(subtotal)#with discount
    tax = (2 * subtotal)/100
    alltotal=tax+subtotal#after having tax
    context={
        'Cart_items':cartlist_items,
        'Total':alltotal,
        'Count':count,
        'Tax':tax,
        'Subtotal':subtotal,
        'WithOutDiscount':rawtotal,
    }
    return render(request,'Cart/htmx-cart.html',context)

# ------------------------- delete product from cart ------------------------- #
def delete_product_cart(request,id):
    if request.method=='POST':
        if request.user.is_authenticated:
            product=get_object_or_404(Products,id=id)#this will find the object from mentioned model ,in a given certain conditions
            cart_items=Cart_Products.objects.get(product=product,user=request.user)
        else:
            carts = Cart.objects.get(cart_id=create_cart_id(request))
            cart_items = Cart_Products.objects.get(product=product, cart=carts)
        cart_items.delete()    
    return redirect(view_cart)



def add_cart_ajax(request):
    total=0
    count=0
    cartlist_items=None
    rawtotal=0
    if request.method == "POST":
        body = json.loads(request.body)
        id = body['id']
        if request.user.is_authenticated:
            cart_products = Cart_Products.objects.get(id=id,user=request.user)
            if cart_products.quantity>=1 :
                if cart_products.quantity<cart_products.product.stock:#checking quantity with stock
                    cart_products.quantity+=1#increasing the quantity 
                    cart_products.save()
                else:
                    print('Stock Not Available')
                    messages.error(request,'Stock Not Available')
            else:
                    pass
            cartlist_items=Cart_Products.objects.filter(is_active=True,user=request.user)
            for i in cartlist_items:
                if int(i.product.discount_price)>0:
                    total+=int(i.product.discount_price*i.quantity)
                    count+=int(i.quantity)
                else:
                    total+=int(i.product.price*i.quantity)
                    count+=int(i.quantity)
                rawtotal+=(i.product.price*i.quantity)
        else:
           cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
           cart_products = Cart_Products.objects.get(id=id,cart=cart_itemsid)
           if cart_products.quantity>=1 :
                if cart_products.quantity<cart_products.product.stock:#checking quantity with stock
                    cart_products.quantity+=1#increasing the quantity 
                    cart_products.save()
                else:
                    messages.error(request,'Stock Not Available')
           else:
                    pass
           cartlist_items=Cart_Products.objects.filter(is_active=True,cart=cart_itemsid)
           for i in cartlist_items:
                if int(i.product.discount_price)>0:
                    total+=int(i.product.discount_price*i.quantity)
                    count+=int(i.quantity)
                else:
                    total+=int(i.product.price*i.quantity)
                    count+=int(i.quantity)
                rawtotal+=(i.product.price*i.quantity)
        subtotal=total
        tax = (2 * subtotal)/100
        alltotal=tax+subtotal

        data = {
        'quantity' : cart_products.quantity,
        'id':id,
        'producttotal':cart_products.quantity*cart_products.product.discount_price,
        'Total':subtotal,
        'Tax':tax,
        'Alltotal':alltotal
        }
        return JsonResponse(data)

def minus_cart_ajax(request):
    total=0
    count=0
    cartlist_items=None
    rawtotal=0                              
    if request.method == "POST":
        body = json.loads(request.body)
        id = body['id']
        if request.user.is_authenticated:
            cart_products = Cart_Products.objects.get(id=id,user=request.user)
            if cart_products.quantity>1 :
                cart_products.quantity-=1#increasing the quantity 
                cart_products.save()
               
            else:
                    pass
            cartlist_items=Cart_Products.objects.filter(is_active=True,user=request.user)
            for i in cartlist_items:
                if int(i.product.discount_price)>0:
                    total+=int(i.product.discount_price*i.quantity)
                    count+=int(i.quantity)
                else:
                    total+=int(i.product.price*i.quantity)
                    count+=int(i.quantity)
                rawtotal+=(i.product.price*i.quantity)
        else:
           cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
           cart_products = Cart_Products.objects.get(id=id,cart=cart_itemsid)
           if cart_products.quantity>=1 :
                cart_products.quantity-=1#increasing the quantity 
                cart_products.save()
                
           else:
                    pass
           cartlist_items=Cart_Products.objects.filter(is_active=True,cart=cart_itemsid)
           for i in cartlist_items:
                if int(i.product.discount_price)>0:
                    total+=int(i.product.discount_price*i.quantity)
                    count+=int(i.quantity)
                else:
                    total+=int(i.product.price*i.quantity)
                    count+=int(i.quantity)
                rawtotal+=(i.product.price*i.quantity)
        subtotal=total
        tax = (2 * subtotal)/100
        alltotal=tax+subtotal
        data = {
        'quantity' : cart_products.quantity,
        'id':id,
        'producttotal':cart_products.quantity*cart_products.product.discount_price,
        'Total':subtotal,
        'Tax':tax,
        'Alltotal':alltotal }
        return JsonResponse(data)


def add_address(request):
    if request.user.is_authenticated:
            wallet_status=request.session['wallet']
            wallet_amount=request.session['amountfromwallet']
            coupon=Coupons.objects.all()
            wallet_Balance=WalletDetails.objects.get(user=request.user)
            total=0
            count=0
            cartlist_items=None
            rawtotal=0
            try:
                cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
                cartlist_items=Cart_Products.objects.filter(is_active=True,user=request.user)
                for i in cartlist_items:
                    if i.product.discount_price>0:
                        total+=(i.product.discount_price*i.quantity)
                        count+=i.quantity
                    else:
                        total+=(i.product.price*i.quantity)
                        count+=i.quantity
                    rawtotal+=(i.product.price*i.quantity)  
            except ObjectDoesNotExist:
                pass
            request.session['original amount']=rawtotal
            request.session['before coupon_amount']=total
            request.session['code']=None
            subtotal=total
            tax = (2 * subtotal)/100
            alltotal=request.session['Totalamount']
            addressDetails = Address.objects.filter(user=request.user)
            if request.method == "POST":
                    Buyername = request.POST["Buyername"]
                    Buyers_Address = request.POST["Buyers_Address"]
                    email = request.POST["email"]
                    phone_number = request.POST["phone_number"]
                    country = request.POST["country"]
                    city = request.POST["city"]
                    state = request.POST["state"]
                    pincode = request.POST["pincode"]
                    if Buyername == "":
                        messages.error(request, "NameField is empty")
                        return render(request, "Cart/AddressAdd.html")
            
                    elif len(Buyername) < 2:
                        messages.error(request, "Name is too short")
                        return render(request, "Cart/AddressAdd.html")

                    elif not Buyername.isalpha():
                        messages.error(request, "Name must contain alphabets")
                        return render(request, "Cart/AddressAdd.html")

                    elif not Buyername.isidentifier():
                        messages.error(request, "Name start must start with alphabets")
                        return render(request, "Cart/AddressAdd.html") 

                    elif email == "":
                        messages.error(request, "Email field is empty")
                        return render(request, "Cart/AddressAdd.html")

                    elif len(email) < 2:
                        messages.error(request, "Email is too short")
                        return render(request, "Cart/AddressAdd.html")

                    elif len(phone_number) < 10:
                        messages.error(request, "Mobile Number should be 10 Digits")
                        return render(request, "Cart/AddressAdd.html")
                    address_data = Address(
                            Buyername=Buyername,
                            email=email,
                            phone_number=phone_number,
                            Buyers_Address=Buyers_Address,
                            city=city,
                            state=state,
                            country=country,
                            user=request.user,
                            pincode=pincode
                        )
                    address_data.save()
                    return redirect(add_address)
            sessiontotal=request.session['Totalamount']#after all Calculations
            usedcoupon=request.session['coupon']
            beforediscountOffer=request.session['original amount']
            discount=beforediscountOffer-sessiontotal
            context={
            'sessiontotal':sessiontotal,#after all applications
            'Cart_items':cartlist_items,
            'Total':alltotal,
            'Count':count,
            'Tax':tax,
            'Subtotal':subtotal,
            'WithOutDiscount':rawtotal,
            'AddressDetails':addressDetails,
            'coupon':coupon,
            'usedcoupon':usedcoupon,
            'discount':discount,#including Coupon and Offer
            'wallet':wallet_Balance,
            'walletstatus':wallet_status,
            'walletamount':wallet_amount
            }
            return render(request,'Cart/AddressAdd.html',context)
    else:
        return redirect('Login')



def apply_coupon(request):
    alltotal=    request.session['Totalamount']
    alltotal=int(alltotal)
    coupon = request.session['coupon']
    if request.method=="POST":
        if coupon == None:
            code = request.POST['code']
            if Coupons.objects.filter(coupon_code__icontains=code):
                if Coupons.objects.filter(coupon_code__icontains=code, is_active=True):
                    obj = Coupons.objects.get(coupon_code=code)
                    if alltotal > obj.min_amount:
                        if alltotal < obj.max_amount:
                            if CouponUsedUsers.objects.filter(coupon=obj.id, user=request.user, status=True):
                                messages.error(request, "Coupon Used")
                            else:
                                request.session['coupon'] = obj.coupon_code
                                discount = int(obj.discount)
                                c = CouponUsedUsers()
                                c.user = request.user
                                c.coupon = obj
                                c.save()
                                request.session['couponid'] = c.id
                                totalamount = alltotal-(alltotal*discount/100)
                                request.session['Totalamount'] = totalamount
                                obj.save()
                        else:
                            messages.error(request, "Exceeded")
                    else:
                        messages.error(request, "minimum needed")
                else:
                    messages.error(request, "Coupon Expired")
            else:
                messages.error(request, "Invalid Coupon")
        else:
            messages.error(request, "Coupon Already Applied")
    return redirect(add_address)


def remove_coupon(request):
    totalamount = request.session['before_coupon_amount']
    to_remove = request.session['coupon']
    coupon_discount_ = Coupons.objects.get(coupon_code__icontains=to_remove)
    remove_ = CouponUsedUsers.objects.filter(
        coupon=coupon_discount_.id, user=request.user)
    remove_.delete()
    discount_price = request.session['Totalamount']
    discount_price = totalamount
    request.session['Totalamount'] = discount_price
    request.session['coupon'] = None
    messages.success(request,'Coupon Removed')
    return redirect(add_address)
    
    







