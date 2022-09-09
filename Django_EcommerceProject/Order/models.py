from django.db import models
from Accounts.models import *
from Cart.models import * 



# Create your models here.
class Payment(models.Model):
    PAYMENT_STATUS =(('Pending','Pending'),
                ("Payment Succesfull","Payment Succesfull"),
                ("Cancel","Cancel"),
                )

    user = models.ForeignKey(Account,on_delete=models.CASCADE, null=True)
    payment_id = models.CharField(max_length=100, null=True)
    payment_method = models.CharField(max_length=100, null=True)
    amount =models.CharField(max_length=100, null=True)
    date =models.DateField(auto_now_add=True)
    payment_status =models.CharField(max_length=100, null=True,choices=PAYMENT_STATUS,default="Pending")
    
    def __str__(self):
        return str(self.payment_method)


 


class Order(models.Model):
    
    
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    payment= models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    total = models.IntegerField(null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    order_id = models.CharField(max_length=30000,null=True)
    date =models.DateField(null=True)
    is_ordered = models.BooleanField(default=False)
    

class Order_Product (models.Model):
    STATUS =(('Order Confirmed','Order Confirmed'),
                ("Shipped","Shipped"),
                ("Out for delivery","Out for delivery"),
                ("Delivered","Delivered"),
                ("Cancelled","Cancelled"),
                ("Returned","Returned"))
    order =models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE,null=True)
    status = models.CharField(max_length=100,choices=STATUS,default='Order Confirmed',null=True)
    quantity = models.IntegerField(null=True)
    product_price = models.FloatField(null=True)
  
    def __str__(self):
        return str(self.product)
































# class payment(models.Model):
#     user = models.ForeignKey(Account,on_delete=models.CASCADE, null=True)
#     payment_id = models.CharField(max_length=100, null=True)
#     payment_method = models.CharField(max_length=100, null=True)
#     amount =models.CharField(max_length=100, null=True)
#     date =models.DateField(auto_now_add=True)
#     status =models.CharField(max_length=100, null=True)
    
#     def __str__(self):
#         return str(self.user)

# class order(models.Model):
#     STATUS =(('order Confirmed','order Confirmed'),
#                 ("shipped","shipped"),
#                 ("out for delivery","out for delivery"),
#                 ("delivered","delivered"),
#                 ("cancelled","cancelled"),
#                 ("returned","returned"))

#     user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
#     payment= models.ForeignKey(payment, on_delete=models.SET_NULL, blank=True, null=True)
#     total = models.IntegerField(null=True)
#     address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
#     order_id = models.CharField(max_length=30000,null=True)
#     date =models.DateField(null=True)
#     status = models.CharField(max_length=100,choices=STATUS,default="order conformed",null=True)
#     is_ordered = models.BooleanField(default=False)
    

#     def __str__(self):
#         return str(self.user) 



# class OrderProduct(models.Model):
#     user                 = models.ForeignKey(Account, on_delete=models.CASCADE)
#     payment              = models.ForeignKey(Payment, on_delete=models.CASCADE)
#     order                = models.ForeignKey(Order, on_delete=models.CASCADE)
#     product              = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity             = models.IntegerField()
#     product_price        = models.FloatField()
#     ordered              = models.BooleanField(default=False)
#     created_at           = models.DateTimeField(auto_now_add=True)
#     updated_at           = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.product.product_name
