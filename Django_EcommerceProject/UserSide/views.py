from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.models import auth
from Accounts.models import* 
from Admin.models import *

from django.views.decorators.cache import cache_control




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    user=Account()
    product=Products.objects.all()
    return render(request,'UserSide/index.html',{'products':product})

def Register(request):
    if 'username' in request.session:
        return redirect(index)
    if request.method == 'POST':
        mobile      = request.POST["phone_number"]
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
                messages.error(request, "username exits")
                return redirect(Register)
            elif email == "":
                messages.error(request, "email field is empty")
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
        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['username'] = username
            messages.success(request, 'You have succesfully logged in', )
            return redirect(loginotp)

        else:
            messages.error(request, "Invalid Credentials")
            print('NOT ABLE TO SIGNIN')
            return redirect(Signin)
    return render(request, 'UserSide/Userlogin-register.html')

def loginotp(request):
    return render(request,'UserSide/loginotp.html')


    

def showParticularproducts(request,id):
    product=Products.objects.get(id=id)
    return render(request,'UserSide/showParticularproducts.html',{'product':product})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Userlogout(request):
    if 'username' in request.session:
       request.session.flush()
    # auth.logout(request)
    return redirect(index)