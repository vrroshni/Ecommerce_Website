from unicodedata import name
from django.urls import path
from . import views
urlpatterns = [


    
    # --------------------------- OrderManagement -------------------------- #
    path('placeorder',views.PlaceOrder,name='PlaceOrder'),
    path('CashonDelivery',views.CashonDelivery,name='CashonDelivery'),
    path('payPalPayment',views.payPalPayment,name='PayPalPayment'),
    path('razorPayPayment',views.razorPayPayment,name='RazorPayPayment'),
    path('success',views.success,name='success'),

    path('orderconfirmed',views.orderConfirmed,name='OrderConfirmed'),
    path('vieworderdetails',views.vieworder_Details,name='ViewOrderDetails'),

    path('cancelorder/<int:id>',views.Cancelorder,name='Cancelorder'),





    










]