from unicodedata import name
from django.urls import path
from . import views
urlpatterns = [
    # --------------------------- View Products in Cart -------------------------- #
    path('',views.view_cart,name='ViewCart'),
    path('addtocart/<int:id>',views.add_ToCart,name='AddToCart'),
    path('decrease_qty/<int:id>',views.decrease_quantity_cart,name='DecreaseQty'),
    path('increase_qty/<int:id>',views.increase_quantity_cart,name='IncreaseQty'),
    path('deletefromcart/<int:id>',views.delete_product_cart,name='DeleteFromCart'),
    
  
  # ----------------------------- checkout happens ----------------------------- #

    path('address',views.add_address,name='AddressAdd'),

    path('applycoupon',views.apply_coupon,name='apply_coupon'),
    path('removecoupon',views.remove_coupon,name='remove_coupon'),
    path('add_cart_ajax/', views.add_cart_ajax, name="add_cart_ajax"),
    path('minus_cart_ajax/', views.minus_cart_ajax, name="minus_cart_ajax"),


  
    
      











]