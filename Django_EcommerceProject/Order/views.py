from ast import Pass
import imp
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
from paypal.standard.forms import PayPalPaymentsForm




# Create your views here.
@login_required(login_url='Index')
@csrf_exempt
def vieworder_Details(request):
   user=request.user
   addressDetails = Address.objects.filter(user=user)
   orderproductdetails=Order_Product.objects.filter(user=user)
   return render(request,'Order/OrderDetails.html',{'OrderProductDetails':orderproductdetails,'AddressDetails':addressDetails})


# --------------- User Manages order Here(Cancelling,Returning) -------------- #
def Cancelorder(request,id):
    orderproductdetails=Order_Product.objects.get(id=id)
    print(orderproductdetails.status)
    orderproductdetails.status='cancelled'
    print('------------------')
    orderproductdetails.save()
    print(orderproductdetails.status)
    return redirect(vieworder_Details)

def order_Returned(request,id):
    orderproductdetails=Order_Product.objects.get(id=id)
    print(orderproductdetails.status)
    orderproductdetails.status='Returned'
    print('------------------')
    orderproductdetails.save()
    print(orderproductdetails.status)
    return redirect(vieworder_Details)    


# -------------------------- Choosing Payment method ------------------------- #
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
        global addressdetails#to access it everywhere
        addressdetails=Address.objects.get(id=address_buyer)
        print(addressdetails.Buyername)
    if pay_mode=='cash':
        return redirect(CashonDelivery)
    if pay_mode=='RazorPay':
        return redirect(razorPayPayment)         
    if pay_mode=='PayPal':
        return redirect(payPalPayment)
    return render (request,"Order/Order_Confirm.html")


# ----------------------- CashonDelivery paymentMethod ----------------------- #
def CashonDelivery(request):
        user = request.user
        cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
        cartlist_items=Cart_Products.objects.filter(cart=cart_itemsid,is_active=True)
        cart_itemcount = cartlist_items.count()
        print(cart_itemcount)
        if request.user.is_authenticated:
            total=0
            quantity=0
            count=0
            for i in cartlist_items:
                    total+=(i.product.price*i.quantity)
                    count+=i.quantity
            tax = (2 * total)/100
            total=tax+total
            # ------------------ saving Whole Order Payment details of CashonDelivey ----------------- #
            payment_obj=Payment()
            payment_obj.user=request.user
            payment_obj. payment_method="cashondelivery"
            payment_obj.payment_id = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            payment_obj.date =date.today()
            payment_obj.amount=total
            payment_obj.save()
            # ------------------ saving Whole Order details of CashonDelivey ----------------- #
            Obj_Order=Order()
            Obj_Order.order_id= str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            Obj_Order.date =date.today()
            Obj_Order.user=request.user
            Obj_Order.total=total
            Obj_Order.address=addressdetails
            Obj_Order.payment=payment_obj
            Obj_Order.is_ordered=True
            Obj_Order.save() 
            # ------------------ saving each product Order details of CashonDelivey ----------------- #
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
            return redirect(orderConfirmed)



@csrf_exempt  
def orderConfirmed(request):
        return render (request,"Order/Order_Confirm.html")


 # -----------------------RazorPay paymentMethod ----------------------- #
def razorPayPayment(request):
        print("HI razor")
        cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
        global cartlist_items
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

            global payment_obj
            payment_obj=Payment()
            payment_obj.user=request.user
            payment_obj. payment_method="razorpay"
            payment_obj.payment_id = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            payment_obj.date =date.today()
            payment_obj.amount=total
            payment_obj.save()





            global Obj_Order
            Obj_Order=Order()
            Obj_Order.order_id= str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            Obj_Order.date =date.today()
            Obj_Order.user=request.user
            Obj_Order.total=total
            Obj_Order.address=addressdetails
            Obj_Order.payment=payment_obj
           
           
            Obj_Order.save()

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
                
            
        if request.method == "POST":

            client = razorpay.Client(auth=("rzp_test_4IGtVl9xeiuWPZ", "ryeb6ntUIE8KhmaWvGzyrBMH"))
            payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
            print(payment)
            return render(request,'Cart/razorpay.html',{'payment': payment}) 
        return render(request,'Cart/razorpay.html') 


@csrf_exempt
def success(request):
    payment_obj.payment_status="Payment Succesfull"
    payment_obj.save(update_fields=['payment_status'])
    print('updated paymentstatus')
    Obj_Order.is_ordered=True
    Obj_Order.save(update_fields=['is_ordered'])

    cartlist_items.delete()
    print('deleted from cart')
    return render(request, "Cart/success.html")





def paypal(request):

    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': order.hotel.price,
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment_cancelled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'UserHome/paypal.html', {'order': order, 'form': form})









# ----------------------- PayPal paymentMethod ----------------------- #
def payPalPayment(request):
        print("HI paypal")
        user = request.user
        print(user)
        cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
        global cartlist_items
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
            global payment_obj
            payment_obj=Payment()
            payment_obj.user=request.user
            payment_obj. payment_method="paypal"
            payment_obj.payment_id = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            payment_obj.date =date.today()
            payment_obj.amount=total
            payment_obj.save()





            global Obj_Order
            Obj_Order=Order()
            Obj_Order.order_id= str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            Obj_Order.date =date.today()
            Obj_Order.user=request.user
            Obj_Order.total=total
            Obj_Order.address=addressdetails
            Obj_Order.payment=payment_obj
            Obj_Order.is_ordered=True
            Obj_Order.save()
            order = get_object_or_404(Order, id=Obj_Order.id)
            host = request.get_host()

            paypal_dict = {
                'business': settings.PAYPAL_RECEIVER_EMAIL,
                'amount': total,
                'item_name': 'Order {}'.format(order.id),
                'invoice': str(order.id),
                'currency_code': 'USD',
                'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
                'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
                'cancel_return': 'http://{}{}'.format(host, reverse('payment_cancelled')),
            }
            form = PayPalPaymentsForm(initial=paypal_dict)
            
            
            
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
            return render (request,'Cart/paypal.html',{'total':total,'order': order,'form': form})   

@csrf_exempt
def payment_done(request):
    payment_obj.payment_status="Payment Succesfull"
    payment_obj.save(update_fields=['payment_status'])
    print('updated paymentstatus')
    Obj_Order.is_ordered=True
    Obj_Order.save(update_fields=['is_ordered'])

    cartlist_items.delete()
    print('deleted from cart')
    return render(request,"Cart/success.html")


@csrf_exempt
def payment_canceled(request):
    return redirect(view_cart)
    