from django.urls import path
from . import views

urlpatterns = [
# -------------------------------- adminlogin||adminlogout -------------------------------- #
        path('',views.adminlogin,name='Adminlogin'),
        path('adminlogout',views.adminlogout,name='AdminLogout'),



# ------------------------------ Admin Dashboard ----------------------------- #
        path('dashboard',views.adminDashboard,name='AdminDashboard'),



# ------------------------- usermangement(adminside) ------------------------- #
        path('usermanagement',views.userdata,name='UserManagement'),
        path('blockuser/<int:id>',views.BlockUser,name='BlockUser'),
        path('unblockuser/<int:id>',views.UnBlockUser,name='UnBlockUser'),


# ------------------------- categorymanagement(adminside) ------------------------- #
        path('AddCategory',views.AddCategory,name='AddCategory'),
        path('ShowCategory',views.ShowCategory,name='ShowCategory'),
        path('DeleteCategory/<int:id>',views.DeleteCategory,name='DeleteCategory'),
        path('EditCategory/<int:id>',views.EditCategory,name='EditCategory'),


# --------------------- subcategorymanagement(adminside) --------------------- #
        path('AddSubCategory',views.AddSubCategory,name='AddSubCategory'),
        path('ShowSubCategory',views.ShowSubCategory,name='ShowSubCategory'),
        path('DeleteSubCategory/<int:id>',views.DeleteSubCategory,name='DeleteSubCategory'),
        path('EditSubCategory/<int:id>',views.EditSubCategory,name='EditSubCategory'),

        
# ----------------------- productmanagement(adminside) ----------------------- #
        path('AddProducts',views.AddProducts,name='AddProducts'),
        path('ShowProducts',views.ShowProducts,name='ShowProducts'),
        path('DeleteProducts/<int:id>',views.DeleteProducts,name='DeleteProducts'),
        path('EditProducts/<int:id>',views.EditProduct,name='EditProducts'),

# ------------------------------ ordermanagement(adminside) ----------------------------- #
        path('Adminvieworder_Details',views.Adminvieworder_Details,name='Adminvieworder_Details'),
        
# --------------------------- changing OrderStatus --------------------------- #
        path('order_Cancelled/<int:id>',views.order_Cancelled,name='order_Cancelled'),
        path('order_Shipped/<int:id>',views.order_Shipped,name='order_Shipped'),
        path('order_Out_For_delivery/<int:id>',views.order_Out_For_delivery,name='order_Out_For_delivery'),
        path('order_Delivered/<int:id>',views.order_Delivered,name='order_Delivered'),
        # path('order_Returned/<int:id>',views.order_Returned,name='order_Returned'),

        



        













]