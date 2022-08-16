from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import*

def autheticatedfor_adminonly(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_superadmin:
            return view_func(request,*args,**kwargs)
        else:
            return render(request,'Admin/restricted.html')
            # return  HttpResponse("<h1>Its restricted for you</h1>")
    return wrapper_func      
