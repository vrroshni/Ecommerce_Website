from unicodedata import name
from django.urls import path
from . import views
urlpatterns = [


    
    # --------------------------- OrderManagement -------------------------- #
    path('placeorder',views.PlaceOrder,name='PlaceOrder'),
    path('payPalPayment',views.payPalPayment,name='PayPalPayment'),
    path('CashOnDelivery',views.CashonDelivery,name='CashonDelivery'),
    path('UseWallet',views.UseWallet,name='UseWallet'),
    path('WalletPayment',views.WalletPayment,name='WalletPayment'),
    path('remove_wallet',views.remove_wallet,name='remove_wallet'),
    path('razorPayPayment',views.razorPayPayment,name='RazorPayPayment'),
    path('success',views.success,name='success'),

    path('orderconfirmed',views.orderConfirmed,name='OrderConfirmed'),
    path('invoice/<int:id>',views.invoice,name='Invoice'),
    path('vieworderdetails',views.vieworder_Details,name='ViewOrderDetails'),

    path('cancelorder/<int:id>',views.Cancelorder,name='Cancelorder'),
    path('returnorder/<int:id>',views.order_Returned,name='OrderReturn'),
    path('cancelorderprofile/<int:id>',views.Cancelorderfromprofile,name='CancelorderProfile'),
    
    path('payment-done/',views.payment_done,name='payment_done'),
    path('payment-cancelled/',views.payment_canceled,name='payment_cancelled'),

      # -------------------------------- applycoupon ------------------------------- #





    










]