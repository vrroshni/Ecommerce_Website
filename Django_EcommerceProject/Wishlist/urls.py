from django.urls import path
from . import views
urlpatterns = [


    
    # --------------------------- WishList Management -------------------------- #
    path('ViewWishlist',views.ViewWishlist,name='ViewWishlist'),
    path('addtowishlist/<int:id>',views.add_to_wishlist,name='AddtoWishlist'),
    path('remove_from_wishlist/<int:id>',views.remove_from_wishlist,name='RemoveFromWishlist'),
    

    










]