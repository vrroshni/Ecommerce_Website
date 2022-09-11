from time import timezone
from django.shortcuts import render,redirect,get_object_or_404
from Admin.models import*
from Accounts.models import*
from Cart.models import*
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from UserSide.views import *
from datetime import date

# Create your views here.





# ----------------- creating separate sessions for each user----------------- #
def create_cart_id(request):
    cartlist_id=request.session.session_key
    if not  cartlist_id:
        cartlist_id=request.session.create()
    return cartlist_id




# ---------------------- funtionality for adding to cart --------------------- #
@login_required(login_url='Index')
def add_ToCart(request,id):
    #product is adding with its id 
    product=Products.objects.get(id=id)
    #if there is chance to have error
    try:
        cart__id=Cart.objects.get(cart_id=create_cart_id(request))#took sessionkeyif it is exists
    except Cart.DoesNotExist:
        cart__id=Cart.objects.create(cart_id=create_cart_id(request))#created sessionkey if it doesnot exists  
        messages.success(request,'Your Product is Added to Your cart')
        cart__id.save()
    # to take objects from Cart_Products
    try:
        cart_items=Cart_Products.objects.get(product=product,cart=cart__id)
        if cart_items.quantity<cart_items.product.stock:#checking quantity with stock
            cart_items.quantity+=1#increasing the quantity 
        messages.success(request,'Your Product is Added to Your cart')
        cart_items.save()
    except Cart_Products.DoesNotExist:#not available,create one
        cart_items=Cart_Products.objects.create(product=product,quantity=1,cart=cart__id)
        cart_items.save()
        messages.success(request,'Your Product is Added to Your cart')
    return redirect(index)



#------------------------ list the items in the cart ------------------------ #
@login_required(login_url='Index')
def view_cart(request,total=0,count=0,cartlist_items=None,rawtotal=0):
    try:
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
    print(rawtotal)#without discount    
    subtotal=total
    print('after discount')
    print(subtotal)#with discount
    tax = (2 * subtotal)/100
    alltotal=tax+subtotal#after having tax
    request.session['Totalamount']=alltotal
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
        cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
        product=get_object_or_404(Products,id=id)#this will find the object from mentioned model ,in a given certain conditions
        cartlist_items=Cart_Products.objects.filter(cart=cart_itemsid,is_active=True,)
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
            print(cart_items.quantity)
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
        'WithOutDiscount':rawtotal


    }
    return render(request,'Cart/htmx-cart.html',context)

# ----------------------- increase the quantity in cart ---------------------- #
def increase_quantity_cart(request,id):
    total=0
    count=0
    cartlist_items=None
    rawtotal=0
    try:
        cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
        product=get_object_or_404(Products,id=id)#this will find the object from mentioned model ,in a given certain conditions
        cartlist_items=Cart_Products.objects.filter(cart=cart_itemsid,is_active=True,)
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
            cart_items.quantity+=1
            print(cart_items.quantity)
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
        'WithOutDiscount':rawtotal


    }
    return render(request,'Cart/htmx-cart.html',context)




# ------------------------- delete product from cart ------------------------- #
def delete_product_cart(request,id):
    if request.method=='POST':
        print("KOOOII")
        cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
        product=get_object_or_404(Products,id=id)#this will find the object from mentioned model ,in a given certain conditions
        cart_items=Cart_Products.objects.get(product=product,cart=cart_itemsid)
        # messages.error(request,'Product is Removed From Cart')
        cart_items.delete()    
    return redirect(view_cart)



@login_required(login_url='Index')
def add_address(request):
        total=0
        count=0
        cartlist_items=None
        rawtotal=0
        if request.user.is_authenticated:
            try:
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
            print(rawtotal)#without discount    
            subtotal=total
            print('after discount')
            print(subtotal)#with discount
            tax = (2 * subtotal)/100
            
            # alltotal=tax+subtotal#after having tax
            alltotal=request.session['Totalamount']
            print(alltotal,'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO')


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
                        messages.error(request, "name start must start with alphabets")
                        return render(request, "Cart/AddressAdd.html") 

                    elif email == "":
                        messages.error(request, "email field is empty")
                        return render(request, "Cart/AddressAdd.html")

                    elif len(email) < 2:
                        messages.error(request, "email is too short")
                        return render(request, "Cart/AddressAdd.html")

                    elif len(phone_number) < 10:
                        messages.error(request, "Mobile Number should be 10 Digits")
                        return render(request, "Cart/AddressAdd.html")

                    elif Address.objects.filter(email=email):
                        messages.error(request, "email already exist try another")
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
            sessiontotal=request.session['Totalamount']
            context={
            'sessiontotal':sessiontotal,
            'Cart_items':cartlist_items,
            'Total':alltotal,
            'Count':count,
            'Tax':tax,
            'Subtotal':subtotal,
            'WithOutDiscount':rawtotal,
            'AddressDetails':addressDetails
            }
        
        return render(request,'Cart/AddressAdd.html',context)
        



def apply_coupon(request):
    if request.method=="POST":
        code=request.POST['code']
        now=date.today()
        print(now)

        if Coupons.objects.filter(coupon_code__iexact=code):
            applying_coupon=Coupons.objects.get(coupon_code__iexact=code)
            if Coupons.objects.filter(coupon_code__iexact=code,valid_from__lte=now,valid_to__gte=now):
                if applying_coupon.user==request.user:
                    print('This Coupon is Already Used,Try Another Valid Coupon')
                    messages.error(request,'This Coupon is Already Used,Try Another Valid Coupon')
                    return redirect(add_address)

                if applying_coupon.is_active == True:
                    discount=int(applying_coupon.discount)
                    print(discount)
                    alltotal=    request.session['Totalamount']
                    totalamount = alltotal-(alltotal*discount/100)
                    print(totalamount)
                    request.session['Totalamount']=totalamount
                    # applying_coupon.is_active=False #for one time use
                    applying_coupon.user=request.user
                    applying_coupon.save()
                    print('coupon applied')
                            
                else:
                    print('coupon invalid')
                    messages.error(request,'This Coupon is Invalid')
                    return redirect(add_address)
    
            else:
                
                messages.error(request,'This Coupon is Expired')
                return redirect(add_address)
     
        else:
            messages.error(request,'This Coupon does not exist')
            return redirect(add_address)
    return redirect(add_address)
    
    







