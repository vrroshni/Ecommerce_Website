from unicodedata import name
from django.urls import path
from . import views
urlpatterns = [
    # --------------------------- View Products in Cart -------------------------- #
    path('',views.view_cart,name='ViewCart'),
    path('addtocart/<int:id>',views.add_ToCart,name='AddToCart'),
    path('decrease_qty/<int:id>',views.decrease_quantity_cart,name='DecreaseQty'),
    path('deletefromcart/<int:id>',views.delete_product_cart,name='DeleteFromCart'),
    
  
  # ----------------------------- checkout happens ----------------------------- #

    path('checkout',views.checkout_products,name='CheckOut'),
    path('address',views.add_address,name='AddressAdd'),
      











]