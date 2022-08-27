from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth import login,authenticate,logout
from Accounts.models import* 
from Admin.models import *
from django.conf import settings
from twilio.rest import Client
from django.views.decorators.cache import cache_control




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    product=Products.objects.all()
    return render(request,'UserSide/index.html',{'products':product})

def Register(request):
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

        if password1 == password2:
            if username == "":
                messages.error(request, "username is empty")
                return redirect(Register)
            elif Account.objects.filter(username=username):
                messages.error(request, "username exists")
                return redirect(Register)
            elif email == "":
                messages.error(request, "email field is empty")
                return redirect(Register)
            elif Account.objects.filter(email=email):
                messages.error(request, "Email exists")
                return redirect(Register)
            
        
            user = Account.objects.create_user(
                    username=username,
                    password=password1,
                    email=email,
                    phone_number=phone_number,
                    first_name=first_name,
                    last_name=last_name

            )
            messages.success(request, 'You have succesfully Registered', )
            user.save()
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
                print('NOT ABLE TO SIGNIN')
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
                auth.login(request,user)
                request.session['username'] = user.username
                return redirect(index)
            else:
                messages.error(request, "Wrong otp")
    
        
    return render(request,'UserSide/loginotp.html')

def userProfileInfo(request):
    user=request.user
    if request.method == 'POST':

        user.first_name=request.POST['first_name']
        user.last_name=request.POST['last_name']
        user.username=request.POST['username']
        user.email=request.POST['email']
        user.phone_number=request.POST['phone_number']
        user.save()
        return redirect(userProfileInfo)
    context={
        'user':user
    }
    return render(request,'UserSide/UserProfile.html',context)





def showParticularproducts(request,id):
    product=Products.objects.get(id=id)
    return render(request,'UserSide/showParticularproducts.html',{'product':product})
    
  

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Userlogout(request):
    # if 'username' in request.session:
    #    request.session.flush()
    auth.logout(request)
    return redirect(index)