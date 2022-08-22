from unicodedata import name
from django.urls import path
from . import views
urlpatterns = [


    
    # --------------------------- OrderManagement -------------------------- #
    path('cashondelivery',views.CashOnDelivery,name='CashOnDelivery'),
    path('vieworderdetails',views.vieworder_Details,name='ViewOrderDetails'),
    path('cancelorder/<int:id>',views.Cancelorder,name='Cancelorder'),


    










]