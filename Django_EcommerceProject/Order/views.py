
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
from django.conf import settings





# Create your views here.
@login_required(login_url='Index')
@csrf_exempt
def vieworder_Details(request):
   user=request.user
   addressDetails = Address.objects.filter(user=user)
   orderproductdetails=Order_Product.objects.filter(user=user,order__is_ordered=True)
   return render(request,'Order/OrderDetails.html',{'OrderProductDetails':orderproductdetails,'AddressDetails':addressDetails})


# --------------- User Manages order Here(Cancelling,Returning) -------------- #
def Cancelorder(request,id):
    orderproductdetails=Order_Product.objects.get(id=id)
    print(orderproductdetails.status)
    print(orderproductdetails.order.total)
    refund_amount=int(orderproductdetails.order.total)
    if orderproductdetails.payment.payment_method=='cashondelivery':
        pass
    else:
        wallet_balance_add=WalletDetails.objects.get(user=request.user)
        wallet_balance_add.balance+=refund_amount           
        
        wallet_balance_add.save()
        getwallet=Wallet.objects.create(user=request.user)
        getwallet.user=request.user
        getwallet.amount=refund_amount
        getwallet.decription_amount="Refund(Order Cancelled)"
        getwallet.save()
        print('credited to wallet')
    orderproductdetails.status='cancelled'
    print('------------------')
    orderproductdetails.save()
    print(orderproductdetails.status)
    return redirect(vieworder_Details)

def order_Returned(request,id):
    orderproductdetails=Order_Product.objects.get(id=id)
    print(orderproductdetails.status)
    print(orderproductdetails.order.total)
    refund_amount=int(orderproductdetails.order.total)
    wallet_balance_add=WalletDetails.objects.get(user=request.user)
    wallet_balance_add.balance+=refund_amount           
    wallet_balance_add.decription_amount="Referral Bonus Credited"
    wallet_balance_add.save()
    getwallet=Wallet.objects.create(user=request.user)
    getwallet.user=request.user
    getwallet.amount=refund_amount
    getwallet.decription_amount="Refund(Order Returned)"
    getwallet.save()
    print('credited to wallet')
    orderproductdetails.status='Returned'
    print('------------------')
    orderproductdetails.save()
    print(orderproductdetails.status)
    return render(request,'Order/Order_Return.html')    

# --------------- User Manages order Here(Cancelling,Returning)(From Profile) -------------- #
def Cancelorderfromprofile(request,id):
    orderproductdetails=Order_Product.objects.get(id=id)
    print(orderproductdetails.status)
    print(orderproductdetails.order.total)
    refund_amount=int(orderproductdetails.order.total)
    if orderproductdetails.payment.payment_method=='cashondelivery':
        pass
    else:
        wallet_balance_add=WalletDetails.objects.get(user=request.user)
        wallet_balance_add.balance+=refund_amount           
        
        wallet_balance_add.save()
        getwallet=Wallet.objects.create(user=request.user)
        getwallet.user=request.user
        getwallet.amount=refund_amount
        getwallet.decription_amount="Refund(Order Cancelled)"
        getwallet.save()
        print('credited to wallet')
    orderproductdetails.status='cancelled'
    print('------------------')
    orderproductdetails.save()
    print(orderproductdetails.status)
    return redirect('UserProfile')

   


# -------------------------- Choosing Payment method ------------------------- #
@login_required(login_url='Index')
def PlaceOrder(request):
    if request.method=='POST':
        pay_mode=request.POST['payment-method']
        try:
            address_buyer=request.POST['addressUsed']
        except:
            messages.error(request,'Add A New  Address')
            return redirect('ViewCart')
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
    if pay_mode=='wallet':
        return redirect(WalletPayment)
    if pay_mode=='RazorPay':
        return redirect(razorPayPayment)         
    if pay_mode=='PayPal':
        return redirect(payPalPayment)
    return render (request,"Order/Order_Confirm.html")



 
def UseWallet(request):
    if request.method=='POST':
        wallet_balance_add=WalletDetails.objects.get(user=request.user)
        getwallet=Wallet.objects.create(user=request.user)
        walletbalance=int(wallet_balance_add.balance)
       
        alltotal=request.session['Totalamount']
        print(alltotal,'alltotallllllllllllllllllll')
        calculation=alltotal
        if walletbalance>=alltotal:
            print(wallet_balance_add.balance,'walletbalance...............')
           
            request.session['amountfromwallet']=alltotal
            request.session['Totalamount']=0
            request.session['wallet']= 'used'

        else:
            alltotal-=wallet_balance_add.balance
            request.session['Totalamount']=alltotal
            request.session['amountfromwallet']=wallet_balance_add.balance
            request.session['wallet']= 'partiallyused'
            
    return redirect(add_address)

def remove_wallet(request):

    alltotal=request.session['Totalamount']
    wallet_amount=request.session['amountfromwallet']
    request.session['Totalamount']=alltotal+wallet_amount
    request.session['wallet']= None

    return redirect(add_address)




# ----------------------- CashonDelivery paymentMethod ----------------------- #

def WalletPayment(request):
    user = request.user
    cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
    cartlist_items=Cart_Products.objects.filter(cart=cart_itemsid,is_active=True)
    cart_itemcount = cartlist_items.count()
    wallet_balance_add=WalletDetails.objects.get(user=request.user)
    getwallet=Wallet.objects.create(user=request.user)
    walletbalance=int(wallet_balance_add.balance)
    print(cart_itemcount)
    if request.user.is_authenticated:
        total=0
        quantity=0
        count=0
        rawtotal=0
        for i in cartlist_items:
                if i.product.discount_price>0:
                    total+=(i.product.discount_price*i.quantity)
                    count+=i.quantity
                else:
                    total+=(i.product.price*i.quantity)
                    count+=i.quantity
                rawtotal+=(i.product.price*i.quantity) 
        print(rawtotal)#without discount    
        subtotal=total
        print('after discount')
        print(subtotal)#with discount
        tax = (2 * subtotal)/100
        request.session['OrderTax']=tax

        # alltotal=tax+subtotal#after having tax
        alltotal=request.session['Totalamount']
        walletamount=request.session['amountfromwallet']
        # ------------------ saving Whole Order Payment details of CashonDelivey ----------------- #
        payment_obj=Payment()
        payment_obj.user=request.user
        payment_obj. payment_method="Wallet"
        payment_obj.payment_id = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
        payment_obj.date =date.today()
        payment_obj.amount=walletamount
        payment_obj.save()
        # ------------------ saving Whole Order details of CashonDelivey ----------------- #
        Obj_Order=Order()
        Obj_Order.order_id= str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
        Obj_Order.date =date.today()
        Obj_Order.user=request.user
        Obj_Order.total=walletamount
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
            orderproduct.status="Order Confirmed"
            orderproduct.save() 
            request.session['order_id']=orderproduct.id 

            product = Products.objects.get(id = x.product.id)
            product.stock -= x.quantity
            product.save()
        cartlist_items.delete()


        walletamount=request.session['amountfromwallet']
        wallet_balance_add.balance-=walletamount
        print(wallet_balance_add.balance,'afterwalletbalance...............')
        wallet_balance_add.save()
        getwallet.decription_amount="debited for purchasing"
        getwallet.amount=walletamount
        getwallet.save()


        return redirect(orderConfirmed)





def CashonDelivery(request):
        wallet_balance_add=WalletDetails.objects.get(user=request.user)
        getwallet=Wallet.objects.create(user=request.user)
        walletbalance=int(wallet_balance_add.balance)
        user = request.user
        cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
        cartlist_items=Cart_Products.objects.filter(cart=cart_itemsid,is_active=True)
        cart_itemcount = cartlist_items.count()
        print(cart_itemcount)
        if request.user.is_authenticated:
            total=0
            quantity=0
            count=0
            rawtotal=0
            for i in cartlist_items:
                    if i.product.discount_price>0:
                        total+=(i.product.discount_price*i.quantity)
                        count+=i.quantity
                    else:
                        total+=(i.product.price*i.quantity)
                        count+=i.quantity
                    rawtotal+=(i.product.price*i.quantity) 
            print(rawtotal)#without discount    
            subtotal=total
            print('after discount')
            print(subtotal)#with discount
            tax = (2 * subtotal)/100
            request.session['OrderTax']=tax
            # alltotal=tax+subtotal#after having tax
            wallet_amount=request.session['amountfromwallet']
            if wallet_amount == None:
                alltotal=request.session['Totalamount']            # ------------------ saving Whole Order Payment details of CashonDelivey ----------------- #
                payment_obj=Payment()
                payment_obj.user=request.user
                payment_obj. payment_method="cashondelivery"
                payment_obj.payment_id = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
                payment_obj.date =date.today()
                payment_obj.amount=alltotal
                payment_obj.save()
                # ------------------ saving Whole Order details of CashonDelivey ----------------- #
                Obj_Order=Order()
                Obj_Order.order_id= str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
                Obj_Order.date =date.today()
                Obj_Order.user=request.user
                Obj_Order.total=alltotal
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
                    orderproduct.status="Order Confirmed"
                    orderproduct.save()
                    request.session['order_id']=orderproduct.id 
                    product = Products.objects.get(id = x.product.id)
                    product.stock -= x.quantity
                    product.save()
             
            cartlist_items.delete()
            try:
                couponid = request.session['couponid']
                print(couponid, 'cccccccccccoooooooooouuuuuupppppppoonnnnnnnn')
                coupon_status = CouponUsedUsers.objects.get(id=couponid)
                coupon_status.status = True
                coupon_status.save()
            except:
                pass


            return redirect(orderConfirmed)

def invoice(request,id):
    today=date.today()
    # Tax=request.session['OrderTax']
    BillOrder=Order_Product.objects.get(id=id)
    print(BillOrder.order.order_id)
    fullproducts=Order_Product.objects.filter(order__order_id=BillOrder.order.order_id)
    print(fullproducts)

    return render(request,'Order/Invoice.html',{'BillOrder':BillOrder,'Fullproducts':fullproducts,'Today':today})

@csrf_exempt  
def orderConfirmed(request):
    order_id=request.session['order_id']
    orderInvoice=Order_Product.objects.get(id=order_id)
    print(orderInvoice,'koooiiiiiiiiiii     INVOICE')
    print(orderInvoice.order.order_id,'koooiiiiiiiiiii     INVOICE')
    
    return render (request,"Order/Order_Confirm.html",{'orderInvoice':orderInvoice})


 # -----------------------RazorPay paymentMethod ----------------------- #
def razorPayPayment(request):
    global payment_obj
    global Obj_Order
    global orderproduct
    
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
        rawtotal=0            
        for i in cartlist_items:
                if i.product.discount_price>0:
                    total+=(i.product.discount_price*i.quantity)
                    count+=i.quantity
                else:
                    total+=(i.product.price*i.quantity)
                    count+=i.quantity
                rawtotal+=(i.product.price*i.quantity) 
        print(rawtotal)#without discount    
        subtotal=total
        print('after discount')
        print(subtotal)#with discount
        tax = (2 * subtotal)/100
        request.session['OrderTax']=tax

        # alltotal=tax+subtotal#after having tax   
        wallet_amount=request.session['amountfromwallet']
        if wallet_amount == None:
            alltotal=request.session['Totalamount']

            amount=alltotal*100   
            amount=int(amount)        
            print(amount) 

            
            payment_obj=Payment()
            payment_obj.user=request.user
            payment_obj. payment_method="razorpay"
            payment_obj.payment_id = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            payment_obj.date =date.today()
            payment_obj.amount=alltotal
            payment_obj.save()

            
            Obj_Order=Order()
            Obj_Order.order_id= str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            Obj_Order.date =date.today()
            Obj_Order.user=request.user
            Obj_Order.total=alltotal
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
                request.session['order_id']=orderproduct.id 

                product = Products.objects.get(id = x.product.id)
                product.stock -= x.quantity
                product.save()
        else:
            alltotal=request.session['Totalamount']

            amount=alltotal*100   
            amount=int(amount)        
            print(amount) 

            
            payment_obj=Payment()
            payment_obj.user=request.user
            payment_obj. payment_method="wallet,razorpay"
            payment_obj.payment_id = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            payment_obj.date =date.today()
            payment_obj.amount=alltotal+wallet_amount
            payment_obj.save()

            
            Obj_Order=Order()
            Obj_Order.order_id= str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            Obj_Order.date =date.today()
            Obj_Order.user=request.user
            Obj_Order.total=alltotal+wallet_amount
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
                request.session['order_id']=orderproduct.id 
                product = Products.objects.get(id = x.product.id)
                product.stock -= x.quantity
                product.save()

    if request.method == "POST":
        client = razorpay.Client(auth=("rzp_test_4IGtVl9xeiuWPZ", "ryeb6ntUIE8KhmaWvGzyrBMH"))
        print('hellooo')
        payment = client.order.create({'amount': amount*100, 'currency': 'INR', 'payment_capture': '1'})        
        return render(request,'Cart/razorpay.html',{'payment': payment,'amount':amount})   
    return render(request,'Cart/razorpay.html',{'amount':amount}) 


@csrf_exempt
def success(request):
    wallet_balance_add=WalletDetails.objects.get(user=request.user)
    getwallet=Wallet.objects.create(user=request.user)
    walletbalance=int(wallet_balance_add.balance)
    print(walletbalance)
    try:
        couponid = request.session['couponid']
        print(couponid, 'cccccccccccoooooooooouuuuuupppppppoonnnnnnnn')
        coupon_status = CouponUsedUsers.objects.get(id=couponid)
        coupon_status.status = True
        coupon_status.save()
    except:
        pass
    request.session['order_id']=orderproduct.id
    statuschangeorder=Order_Product.objects.filter(order__order_id=orderproduct.order.order_id)
    print(statuschangeorder,'productssssssssssssssssssss')
    for x in statuschangeorder:
        print('each product status')
        x.status="Order Confirmed"
        x.save(update_fields=['status'])

    payment_obj.payment_status="Payment Succesfull"
    payment_obj.save(update_fields=['payment_status'])
    print('updated paymentstatus')
    Obj_Order.is_ordered=True
    Obj_Order.save(update_fields=['is_ordered'])
    cartlist_items.delete()
    print('deleted from cart')

    walletstatus=request.session['wallet']
    if walletstatus != None:
        walletamount=request.session['amountfromwallet']
        wallet_balance_add.balance-=walletamount
        print(wallet_balance_add.balance,'afterwalletbalance...............')
        wallet_balance_add.save()
        getwallet.decription_amount="Debited for purchasing"
        getwallet.amount=walletamount
        getwallet.save()


    return redirect(orderConfirmed)


# ----------------------- PayPal paymentMethod ----------------------- #
def payPalPayment(request):
        global payment_obj
        global Obj_Order
        global orderproduct
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
            rawtotal=0
            
            for i in cartlist_items:
                    if i.product.discount_price>0:
                        total+=(i.product.discount_price*i.quantity)
                        count+=i.quantity
                    else:
                        total+=(i.product.price*i.quantity)
                        count+=i.quantity
                    rawtotal+=(i.product.price*i.quantity) 
            print(rawtotal)#without discount    
            subtotal=total
            print('after discount')
            print(subtotal)#with discount
            tax = (2 * subtotal)/100
            request.session['OrderTax']=tax
            # alltotal=tax+subtotal#after having tax
            wallet_amount=request.session['amountfromwallet']
            if wallet_amount == None:   
                alltotal=request.session['Totalamount']
 
                payment_obj=Payment()
                payment_obj.user=request.user
                payment_obj. payment_method="paypal"
                payment_obj.payment_id = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
                payment_obj.date =date.today()
                payment_obj.amount=alltotal
                payment_obj.save()


                Obj_Order=Order()
                Obj_Order.order_id= str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
                Obj_Order.date =date.today()
                Obj_Order.user=request.user
                Obj_Order.total=alltotal
                Obj_Order.address=addressdetails
                Obj_Order.payment=payment_obj
                Obj_Order.save()
            else:
                alltotal=request.session['Totalamount'] 

                payment_obj=Payment()
                payment_obj.user=request.user
                payment_obj. payment_method="wallet,paypal"
                payment_obj.payment_id = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
                payment_obj.date =date.today()
                payment_obj.amount=alltotal+wallet_amount
                payment_obj.save()

                
                Obj_Order=Order()
                Obj_Order.order_id= str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
                Obj_Order.date =date.today()
                Obj_Order.user=request.user
                Obj_Order.total=alltotal+wallet_amount
                Obj_Order.address=addressdetails
                Obj_Order.payment=payment_obj
                Obj_Order.save()

            order = get_object_or_404(Order, id=Obj_Order.id)
            host = request.get_host()

            paypal_dict = {
                'business': settings.PAYPAL_RECEIVER_EMAIL,
                'amount': alltotal,
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
                global orderproduct
                orderproduct = Order_Product()

                orderproduct.user=request.user
                orderproduct.order=Obj_Order
                orderproduct.quantity =x.quantity
                orderproduct.product=x.product
                orderproduct.payment=payment_obj
                orderproduct.product_price=x.product.price
                orderproduct.save()
                request.session['order_id']=orderproduct.id 
                product = Products.objects.get(id = x.product.id)
                product.stock -= x.quantity
                product.save()
            return render (request,'Cart/paypal.html',{'total':total,'order': order,'form': form,'Alltotal':alltotal})   





@csrf_exempt
def payment_done(request):

    wallet_balance_add=WalletDetails.objects.get(user=request.user)
    getwallet=Wallet.objects.create(user=request.user)
    walletbalance=int(wallet_balance_add.balance)


    try:
        couponid = request.session['couponid']
        print(couponid, 'cccccccccccoooooooooouuuuuupppppppoonnnnnnnn')
        coupon_status = CouponUsedUsers.objects.get(id=couponid)
        coupon_status.status = True
        coupon_status.save()
    except:
        pass
    request.session['order_id']=orderproduct.id
    statuschangeorder=Order_Product.objects.filter(order__order_id=orderproduct.order.order_id)
    print(statuschangeorder,'productssssssssssssssssssss')
    for x in statuschangeorder:
        print('each product status')
        x.status="Order Confirmed"
        x.save(update_fields=['status'])
    payment_obj.payment_status="Payment Succesfull"
    payment_obj.save(update_fields=['payment_status'])
    print('updated paymentstatus')
    Obj_Order.is_ordered=True
    Obj_Order.save(update_fields=['is_ordered'])
   
    walletstatus=request.session['wallet']
    if walletstatus != None:

        walletamount=request.session['amountfromwallet']
        wallet_balance_add.balance-=walletamount
        print(wallet_balance_add.balance,'afterwalletbalance...............')
        wallet_balance_add.save()
        getwallet.decription_amount="Debited for purchasing"
        getwallet.amount=walletamount
        getwallet.save()
    cartlist_items.delete()
    print('deleted from cart')
    return redirect(orderConfirmed)

@csrf_exempt
def payment_canceled(request):
    return redirect(view_cart)
    