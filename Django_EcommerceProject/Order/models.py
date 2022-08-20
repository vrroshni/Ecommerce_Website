from django.db import models

# Create your models here.
# class Order(models.Model):
#     STATUS = (
#         ('Order Confirmed', 'Order Confirmed'),
#         ('Accepted', 'Accepted'),
#         ('Completed', 'Completed'),
#         ('Cancelled', 'Cancelled'),
#         ('Returned', 'Returned'),
#     )
#     user                 = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
#     payment              = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
#     order_number         = models.CharField(max_length=20)
#     first_name           = models.CharField(max_length=50)
#     last_name            = models.CharField(max_length=50, null=True)
#     phone                = models.CharField(max_length=20)
#     email                = models.EmailField(max_length=50)
#     address_line_1       = models.CharField(max_length=50)
#     address_line_2       = models.CharField(max_length=50, null=True)
#     country              = models.CharField(max_length=50)
#     state                = models.CharField(max_length=50)
#     city                 = models.CharField(max_length=50)
   
#     order_total          = models.FloatField()
#     tax                  = models.FloatField()
#     status               = models.CharField(max_length=20, choices=STATUS, default='Order Confirmed')
#     ip                   = models.CharField(blank=True, max_length=20, null=True)
#     is_ordered           = models.BooleanField(default=False)
#     created_at           = models.DateTimeField(auto_now_add=True)
#     updated_at           = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.first_name


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