from django.db import models
from Accounts.models import *
from Admin.models import *

# Create your models here.
class Wishlist(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    wished_product=models.ForeignKey(Products,on_delete=models.CASCADE)
    added_date=models.DateTimeField(auto_now_add=True)