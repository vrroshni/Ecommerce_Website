from ast import Pass
from pickle import FALSE
from django.shortcuts import render,redirect
from Cart.models import*
from Order.models import*
from datetime import date
import datetime
from Cart.views import *
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required




# Create your views here.
@login_required(login_url='Index')
@csrf_exempt
def vieworder_Details(request):
   user=request.user
   addressDetails = Address.objects.filter(user=request.user)

   orderproductdetails=Order_Product.objects.filter(user=user)
   return render(request,'Order/OrderDetails.html',{'OrderProductDetails':orderproductdetails,'AddressDetails':addressDetails})


def Cancelorder(request,id):
    user=request.user
    orderproductdetails=Order_Product.objects.get(id=id)
    print(orderproductdetails.status)
    orderproductdetails.status='cancelled'
    print('------------------')
    orderproductdetails.save()
    print(orderproductdetails.status)

    return redirect(vieworder_Details)

    



@login_required(login_url='Index')
def PlaceOrder(request):
    if request.method=='POST':
        pay_mode=request.POST['payment-method']
        address_buyer=request.POST['addressUsed']
        if pay_mode=="":
            messages.error(request,"Choosing A Payment Method is Mandatory")
            return redirect(PlaceOrder)
        if address_buyer=="":
            messages.error(request,"Please Choose Your Address")
            return redirect(PlaceOrder)

        print(address_buyer)
        addressdetails=Address.objects.get(id=address_buyer)
        print(addressdetails.Buyername)
        
    if pay_mode=='cash':

        print("HI")
        user = request.user
        print(user)
        cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
        cartlist_items=Cart_Products.objects.filter(cart=cart_itemsid,is_active=True)

        print(cart_itemsid)
        print(cartlist_items)
     

        cart_itemcount = cartlist_items.count()
        print(cart_itemcount)
        

        if request.user.is_authenticated:
         
            total=0
            quantity=0
            count=0
            
            for i in cartlist_items:
                    total+=(i.product.price*i.quantity)
                    count+=i.quantity
    
            subtotal=total
            
            tax = (2 * total)/100
            total=tax+total
            
            print(total)
            print('printed')
            payment_obj=Payment()
            payment_obj.user=request.user
            payment_obj. payment_method="cashondelivery"
            payment_obj.payment_id = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            payment_obj.date =date.today()
            payment_obj.amount=total
            payment_obj.save()






            Obj_Order=Order()
            Obj_Order.order_id= str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            Obj_Order.date =date.today()
            Obj_Order.user=request.user
            Obj_Order.total=total
            Obj_Order.address=addressdetails
            Obj_Order.payment=payment_obj
            Obj_Order.is_ordered="True"
            Obj_Order.save()
            
            
            
            print("hello")
           
            for x in cartlist_items:
                orderproduct = Order_Product()

                orderproduct.user=request.user
                orderproduct.order=Obj_Order
                orderproduct.quantity =x.quantity
                orderproduct.product=x.product
                orderproduct.payment=payment_obj
                orderproduct.product_price=x.product.price
                orderproduct.save() 
                product = Products.objects.get(id = x.product.id)
                product.stock -= x.quantity
                product.save()
                
            cartlist_items.delete()
            print('deleted from cart')
            
    if pay_mode=='RazorPay':
        print("HI razor")
        user = request.user
        print(user)
        cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
        cartlist_items=Cart_Products.objects.filter(cart=cart_itemsid,is_active=True)

        print(cart_itemsid)
        print(cartlist_items)

        cart_itemcount = cartlist_items.count()
        print(cart_itemcount)
        

        if request.user.is_authenticated:
        
            total=0
            quantity=0
            count=0
            
            for i in cartlist_items:
                    total+=(i.product.price*i.quantity)
                    count+=i.quantity
    
            subtotal=total
            
            tax = ((2 * total)/100)
            amount=tax+total
            amount=int(amount)*100
            
            print(amount)
            print('printed')
            payment_obj=Payment()
            payment_obj.user=request.user
            payment_obj. payment_method="razorpay"
            payment_obj.payment_id = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            payment_obj.date =date.today()
            payment_obj.amount=total
            payment_obj.save()






            Obj_Order=Order()
            Obj_Order.order_id= str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            Obj_Order.date =date.today()
            Obj_Order.user=request.user
            Obj_Order.total=total
            Obj_Order.address=addressdetails
            Obj_Order.payment=payment_obj
            Obj_Order.is_ordered="True"
            Obj_Order.save()
            
            
            
            print("hello")
           
            for x in cartlist_items:
                orderproduct = Order_Product()

                orderproduct.user=request.user
                orderproduct.order=Obj_Order
                orderproduct.quantity =x.quantity
                orderproduct.product=x.product
                orderproduct.payment=payment_obj
                orderproduct.product_price=x.product.price
                orderproduct.save() 
                product = Products.objects.get(id = x.product.id)
                product.stock -= x.quantity
                product.save()
                
            cartlist_items.delete()
            print('deleted from cart')

            client = razorpay.Client(auth=("rzp_test_u6wVuQH1CZfo2w", "exxRBF8nxJAEPS7EWtytlLCk"))
            payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
            print(payment)
            return render(request,'Cart/razorpay.html',{'payment': payment})
            
    if pay_mode=='PayPal':
        print("HI paypal")
        user = request.user
        print(user)
        cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
        cartlist_items=Cart_Products.objects.filter(cart=cart_itemsid,is_active=True)

        print(cart_itemsid)
        print(cartlist_items)

        cart_itemcount = cartlist_items.count()
        print(cart_itemcount)
        

        if request.user.is_authenticated:
       
            total=0
            quantity=0
            count=0
            
            for i in cartlist_items:
                    total+=(i.product.price*i.quantity)
                    count+=i.quantity
    
            subtotal=total
            
            tax = (2 * total)/100
            total=tax+total
            
            print(total)
            print('printed')
            payment_obj=Payment()
            payment_obj.user=request.user
            payment_obj. payment_method="paypal"
            payment_obj.payment_id = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            payment_obj.date =date.today()
            payment_obj.amount=total
            payment_obj.save()






            Obj_Order=Order()
            Obj_Order.order_id= str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            Obj_Order.date =date.today()
            Obj_Order.user=request.user
            Obj_Order.total=total
            Obj_Order.address=addressdetails
            Obj_Order.payment=payment_obj
            Obj_Order.is_ordered="True"
            Obj_Order.save()
            
            
            
            print("hello")
           
            for x in cartlist_items:
                orderproduct = Order_Product()

                orderproduct.user=request.user
                orderproduct.order=Obj_Order
                orderproduct.quantity =x.quantity
                orderproduct.product=x.product
                orderproduct.payment=payment_obj
                orderproduct.product_price=x.product.price
                orderproduct.save() 
                product = Products.objects.get(id = x.product.id)
                product.stock -= x.quantity
                product.save()
                
            cartlist_items.delete()
            print('deleted from cart')
            return render (request,'Cart/paypal.html',{'total':total})




            
    return render (request,"Order/Order_Confirm.html")


@csrf_exempt
def orderConfirmed(request):
        return render (request,"Order/Order_Confirm.html")


   
    
   

