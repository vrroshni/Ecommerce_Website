from django.urls import path
from . import views
urlpatterns = [
    # ------------------------------- Landing page ------------------------------- #
    path('',views.index,name='Index'),#product are dispalyed 

    # ----------------------------- Authorizing User ----------------------------- #
    path('login',views.Signin,name='Login'),
    path('loginotp/<int:id>/',views.loginotp,name='loginOtp'),
    path('logout',views.Userlogout,name='Userlogout'),
    path('Profile',views.userProfileInfo,name='UserProfile'),
    # path('EditProfile',views.EditProfile,name='EditUserProfile'),


    # ----------------------------- Registering User ----------------------------- #
    path('register',views.Register,name='Register'),

    # --------------------------- products in Userside --------------------------- #
    path('showparticularproducts/<int:id>',views.showParticularproducts,name='showParticularproducts'),
    path('shop',views.shop,name='Shop'),
    path('subshop',views.subshop,name='SubShop'),

    

    
]
