from django.shortcuts import render,redirect,get_object_or_404
from Admin.models import*
from Accounts.models import*
from Cart.models import*
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib import messages

# Create your views here.





# ----------------- creating separate sessions for each user----------------- #
def create_cart_id(request):
    cartlist_id=request.session.session_key
    if not  cartlist_id:
        cartlist_id=request.session.create()
    return cartlist_id




# ---------------------- funtionality for adding to cart --------------------- #
def add_ToCart(request,id):
    #product is adding with its id 
    product=Products.objects.get(id=id)
    #if there is chance to have error
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
        cart_items.save()
    except Cart_Products.DoesNotExist:#not available,create one
        cart_items=Cart_Products.objects.create(product=product,quantity=1,cart=cart__id)
        cart_items.save()
    return redirect('ViewCart')



#------------------------ list the items in the cart ------------------------ #
def view_cart(request,total=0,count=0,cartlist_items=None):
    try:
        cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
        cartlist_items=Cart_Products.objects.filter(cart=cart_itemsid,is_active=True)
        for i in cartlist_items:
                    total+=(i.product.price*i.quantity)
                    count+=i.quantity
    except ObjectDoesNotExist:
           pass
    subtotal=total
    tax = (2 * total)/100
    total=tax+total
    return render(request,'Cart/ViewCart.html',{'Cart_items':cartlist_items,'Total':total,'Count':count,'Tax':tax,'Subtotal':subtotal})




# ----------------------- decrease the quantity in cart ---------------------- #
def decrease_quantity_cart(request,id):
    cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
    product=get_object_or_404(Products,id=id)#this will find the object from mentioned model ,in a given certain conditions
    cart_items=Cart_Products.objects.get(product=product,cart=cart_itemsid)
    if cart_items.quantity>1:
        cart_items.quantity-=1
        cart_items.save()
    else:
        cart_items.delete()
    return redirect(view_cart)




# ------------------------- delete product from cart ------------------------- #
def delete_product_cart(request,id):
    cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
    product=get_object_or_404(Products,id=id)#this will find the object from mentioned model ,in a given certain conditions
    cart_items=Cart_Products.objects.get(product=product,cart=cart_itemsid)
    cart_items.delete()
    return redirect(view_cart)










def add_address(request):
        total=0
        count=0
        cartlist_items=None
    

        if request.user.is_authenticated:
            try:
                cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
                cartlist_items=Cart_Products.objects.filter(cart=cart_itemsid,is_active=True)
                for i in cartlist_items:
                            total+=(i.product.price*i.quantity)
                            count+=i.quantity
            except ObjectDoesNotExist:
                pass
            subtotal=total
            tax = (2 * total)/100
            total=tax+total
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
                        )
                    address_data.save()
                    return redirect(add_address)
        
        return render(request,'Cart/AddressAdd.html',{'Cart_items':cartlist_items,'Total':total,'Count':count,'Tax':tax,'Subtotal':subtotal,'AddressDetails':addressDetails})
        




    







