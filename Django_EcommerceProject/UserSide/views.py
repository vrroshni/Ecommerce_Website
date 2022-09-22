from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from Accounts.models import* 
from Admin.models import *
from Order.models import *
from Cart.views import *
from django.conf import settings
from twilio.rest import Client
from django.views.decorators.cache import cache_control
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max, Min
from datetime import date



#this function will save discount price in database 

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    # -------------------- deactivate coupon after expiry date ------------------- #
    now=date.today()
    coupons=Coupons.objects.filter(valid_to__lte=now)
    for y in coupons:
        y.active=False
        y.save()
    allproduct=Products.objects.all()
    allcategory=Categories.objects.all()
    #looping through all products to calculate its discount Price
    for x in allproduct:
        list=[]
        # ------------------------ checking for category offer ----------------------- #
        try:
            category_offer=Categoryoffer.objects.get(category=x.category,is_active =True)
            list.append(category_offer.discount)
        except ObjectDoesNotExist:
            pass
        # ------------------------ checking for subcategory offer ----------------------- #
        try:
            subcategory_offer=SubCategoryoffer.objects.get(subcategory=x.subcategories,is_active =True)
            list.append(subcategory_offer.discount)
        except ObjectDoesNotExist:
            pass
        # ------------------------ checking for Product offer ----------------------- #
        try:
            product_offer=Productoffer.objects.get(product=x.id,is_active =True)
            list.append(product_offer.discount)
        except ObjectDoesNotExist:
            pass
        #setting discount price zero,if we remove any ofers by chance
        #every time we runserver offers will be setted once again        
        x.discount_price=0
        #incase if there is no any offers for this product(if list is empty) 
        if list:
            maxoffer=max(list)#finding minimum amount of offers from category,subcategory,products to apply
            x.discount_percentage=maxoffer#assigning  discount percentage
            x.discount_price=x.price-(x.price*maxoffer/100)#calculating amount after discount
            x.save()
        else:
            pass
    return render(request,'UserSide/index.html',{'products':allproduct,'Categories':allcategory})

    

def Register(request):
    referredPerson=None
    code_reffered=None
    if 'username' in request.session:
        return redirect(index)
    if request.method == 'POST':
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        phone_number = request.POST["phone_number"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        codepattern=first_name
        referral_code=codepattern.upper()+"REFER"+"500"
        print(referral_code)
        if password1 == password2:
            if username == "":
                messages.error(request, "username is empty")
                return redirect(Register)
            elif Account.objects.filter(username=username):
                messages.error(request, "username exists")
                return redirect(Register)
            elif email == "":
                messages.error(request, "Email field is empty")
                return redirect(Register)
            elif Account.objects.filter(email=email):
                messages.error(request, "Email exists")
                return redirect(Register)
            try:
                code_reffered=request.POST["referral_code"]
                referredPerson=Account.objects.get(referral_code__iexact=code_reffered)
                if referredPerson != None:
                    try:
                        wallet_balance_add=WalletDetails.objects.get(user=referredPerson)
                        wallet_balance_add.balance+=50          
                        wallet_balance_add.save()
                        getwallet=Wallet.objects.create(user=referredPerson)
                        getwallet.user=referredPerson
                        getwallet.amount=50
                        getwallet.decription_amount="Referral Bonus Credited"
                        getwallet.save()
                        print('credited to wallet')
                        messages.success(request,'refferral  applied')
                    except:
                       pass
                else:
                    messages.error(request,"enter the correct refferral code")
            except:
                pass
            user = Account.objects.create_user(
                    username=username,
                    password=password1,
                    email=email,
                    phone_number=phone_number,
                    first_name=first_name,
                    last_name=last_name,
            )
            if code_reffered != None:
                user.ref_active=True
                createdwallet=Wallet.objects.create(user=user,decription_amount="Wallet Created,")
                WalletDetails.objects.create(user=user,wallet=createdwallet)
            else:
                createdwallet=Wallet.objects.create(user=user,decription_amount="Referral Bonus ",amount=50)
                WalletDetails.objects.create(user=user,wallet=createdwallet,balance=50)
            user.code_reffered=code_reffered
            user.referral_code=referral_code
            user.save()           
            messages.success(request, 'You have succesfully Registered')
            return redirect(Signin)
    return render(request,'UserSide/Userlogin-register.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Signin(request):
    if 'username' in request.session:
        return redirect(index)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        usserblockstaus=Account.objects.get(username=request.POST.get('username'))
        if usserblockstaus.is_active==True:
            user = authenticate(username=username, password=password)
            if user is not None:
                    phone=Account.objects.get(username=request.POST.get('username'))
                    phone_number=phone.phone_number
                    account_sid     = settings.ACCOUNT_SID
                    auth_token      = settings.AUTH_TOKEN
                    client = Client(account_sid, auth_token)
                    verification = client.verify \
                                            .v2 \
                                            .services(settings.SERVICE_ID) \
                                            .verifications \
                                            .create(to=f'{settings.COUNTRY_CODE}{phone_number}', channel='sms')
                    print(verification.status)
                    messages.success(request, 'Otp sent Succesfully to your Registered Mobile number' )
                    return redirect(f'loginotp/{phone.id}/')
            else:
                messages.error(request, "Invalid Credentials")
        else:
            messages.error(request,'You are blocked!!')        
    return render(request,'UserSide/login.html')


def loginotp(request,id):
    if request.method == 'POST':
        user      = Account.objects.get(id=id)
        phone_number=user.phone_number
        otpvalue  = request.POST.get('otp')
        if otpvalue=="":
            messages.error(request,'Enter The Otp!!!')
            
        else:    
            account_sid     = settings.ACCOUNT_SID
            auth_token      = settings.AUTH_TOKEN
            client = Client(account_sid, auth_token)

            verification_check = client.verify \
                                    .v2 \
                                    .services(settings.SERVICE_ID) \
                                    .verification_checks \
                                    .create(to=f'{settings.COUNTRY_CODE}{phone_number}', code=otpvalue)

            print(verification_check.status)
            if verification_check.status=='approved':
                try:
                    carts =Cart.objects.get(cart_id=request.session.session_key)
                    carts_item = Cart_Products.objects.filter(cart_id = carts) 
                    users_item = Cart_Products.objects.filter(user = user)
                    for x in carts_item:#if multiple item in cart
                        a=0
                        if users_item:
                                for y in users_item:#check each items in users_items 
                                    if  x.product == y.product:#if product in both carts_items from sessions id and users  product from cart_item(models) matches
                                        y.quantity += x.quantity#product items quantity will be sum of .....
                                        x.delete()#delete the carts_item  
                                        y.save()
                                        a=1
                                        break
                                    if a==0:# to add if different product to user cart 
                                        x.user=user
                                        x.save()
                                        auth.login(request,user)
                                        return redirect(index)
                        else:
                            x.user=user
                            x.save()
                            auth.login(request,user)
                            return redirect(index)
                except:
                    auth.login(request,user)
                    request.session['username'] = user.username
                    return redirect(index)               
            else:
                messages.error(request, "Wrong otp")    
    return render(request,'UserSide/loginotp.html')
    
@login_required(login_url='Index')
def userProfileInfo(request):
    user=request.user
    orderproductdetails=Order_Product.objects.filter(user=user,order__is_ordered=True)
    addressDetails = Address.objects.filter(user=request.user)
    walletdetails=Wallet.objects.filter(user=user).order_by('id')
    walletbalance=WalletDetails.objects.get(user=user)
    if request.method == 'POST':
        user.first_name=request.POST['first_name']
        user.last_name=request.POST['last_name']
        user.username=request.POST['username']
        user.email=request.POST['email']
        user.phone_number=request.POST['phone_number']
        if user.first_name =="" or  user.last_name =="" or  user.username =="" or user.email =="":
            messages.error(request,"Fields Can't be Empty") 
            return redirect(userProfileInfo)
        user.save()
        return redirect(userProfileInfo)

    context={
        'user':user,
        'OrderProductDetails':orderproductdetails,
        'AddressDetails':addressDetails,
        'walletdetails':walletdetails,
        'walletbalance':walletbalance
    }
    return render(request,'UserSide/UserProfile.html',context)


def showParticularproducts(request,id):
    product=Products.objects.get(id=id)
    allproducts=Products.objects.filter(category=product.category)
    return render(request,'UserSide/showParticularproducts.html',{'product':product,'Allproducts':allproducts})
    

def shop(request):
    category=request.GET.get('category')
    subcategory=None
    if category == None:
        product=Products.objects.all()
    else:
        subcategory=SubCategories.objects.filter(category__title=category)
        product=Products.objects.filter(category__title=category)
    min_price = Products.objects.all().aggregate(Min('price'))
    max_price = Products.objects.all().aggregate(Max('price'))
    FilterPrice = request.GET.get('FilterPrice')
    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        product = Products.objects.filter(price__lte = Int_FilterPrice)
 
    categories=Categories.objects.all()

    context={
        'Categories':categories,
        'Subcategories':subcategory,
        'Products':product,
        'min_price':min_price,
        'max_price':max_price,
		'FilterPrice':FilterPrice,
        
    }
    return render(request,'UserSide/shop.html',context)


def subshop(request):
    categories=Categories.objects.all()
    subcategory=request.GET.get('subcategory')
    min_price = Products.objects.all().aggregate(Min('price'))
    max_price = Products.objects.all().aggregate(Max('price'))
    print(min_price)
    print(max_price)

    FilterPrice = request.GET.get('FilterPrice')
    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        product = Products.objects.filter(price__lte = Int_FilterPrice)

    if subcategory != None:
        product=Products.objects.filter(subcategories__title=subcategory)
    context={
        'Products':product,
        'Categories':categories,
        'min_price':min_price,
        'max_price':max_price,
		'FilterPrice':FilterPrice,
    }
    return render(request,'UserSide/shop.html',context)





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Userlogout(request):
    auth.logout(request)
    return redirect(index)