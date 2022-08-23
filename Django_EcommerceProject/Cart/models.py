from django.db import models
from Admin.models  import  *
from Accounts.models import *


# Create your models here.


class Cart(models.Model):
    cart_id         = models.CharField(max_length=50,unique=True)
    date_added      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class Cart_Products(models.Model):
    user            = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product         = models.ForeignKey(Products, on_delete=models.CASCADE)
    cart            = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity        = models.PositiveIntegerField()
    is_active       = models.BooleanField(default=True)
   

    def __str__(self):
        return self.product.product_name

    def sub_total(self):
        return self.product.price * self.quantity


# class UserProfile(models.Model):
#     user                        = models.ForeignKey(Account, on_delete=models.CASCADE)
#     address_line_1              = models.CharField(max_length=100, blank=True)
#     address_line_2              = models.CharField(max_length=100, blank=True)
#     profile_picture             = models.ImageField(null=True ,blank=True,  upload_to='photos/userprofile')
#     city                        = models.CharField( max_length=20)
#     state                       = models.CharField( max_length=20)
#     country                     = models.CharField( max_length=20)

#     def __str__(self):
#         return self.user.first_name



class Address(models.Model):
    user                        = models.ForeignKey(Account, on_delete=models.CASCADE)
    Buyername                   = models.CharField(max_length=50, blank=True)
    phone_number                = models.CharField(max_length=25)
    email                       = models.EmailField(max_length=50, null=True)
    Buyers_Address              = models.CharField(max_length=100, blank=True)      
    pincode                     = models.IntegerField(null=True)
    city                        = models.CharField( max_length=20)
    state                       = models.CharField( max_length=100,default='Kerala')
    country                     = models.CharField( max_length=20,default='India')

    def __str__(self):
        return self.Buyername                   