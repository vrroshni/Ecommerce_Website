from unicodedata import category
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.models import auth,User
from Accounts.models import *
from .models import *
from django.views.decorators.cache import cache_control
from .decorators import*




# Create your views here.


# ---------------------------------------------------------------------------- #
#                           admin login here. session is created                         #
# ---------------------------------------------------------------------------- #
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminlogin(request):
    if 'username' in request.session:
        return redirect(userdata)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_superadmin:
                # login(request,user)
                auth.login(request,user)
                request.session['username'] = username
                messages.success(request, 'Welcome !!!')
                return redirect(userdata)
            else :
                messages.error(request,'You are not authenticated to view coming pages')
        else:
                messages.error(request, '*Invalid Username or Password')
                return redirect(adminlogin)
       
    return render(request,'Admin/adminlogin.html')


# ------------------- users data will be seen in this page ------------------- #
@autheticatedfor_adminonly
def userdata(request):
    data = Account.objects.all()
    return render(request, 'Admin/adminuserdata.html', {'datas': data})  

# --------------------------- for blocking User --------------------------- #
def BlockUser(request, id):
    mydata = Account.objects.get(id=id)
    mydata.is_active=False
    mydata.save()
    messages.success(request, 'User is Blocked Successfully')
    return redirect(userdata)


# --------------------------- for Unblocking User --------------------------- #
def UnBlockUser(request, id):
    mydata = Account.objects.get(id=id)
    mydata.is_active=True
    mydata.save()
    messages.error(request, 'User is UnBlocked Successfully')
    return redirect(userdata)

# ---------------------------- CategoryManagement ---------------------------- #
# --------------------------- Adding a new category -------------------------- #
@autheticatedfor_adminonly
def AddCategory(request):
    if request.method == 'POST':
            title = request.POST['title']
            description = request.POST['description']
            if Categories.objects.filter(title=title).exists():
                messages.error(request, "This Category already Exists")
                print('This category exits')
                return redirect(AddCategory)
            if title =='' :
                messages.error(request, "Category fields cannot be blank")
                print('Filed blank')
                return redirect(AddCategory)
        
        
            category = Categories.objects.create(
                        title=title,description=description)
            category.save()
            messages.success(request, 'Category has been Created Succesfully')
            return redirect(ShowCategory)
    
    return render(request,'Admin/addCategory.html')

# ------------------------- Showing Whole categories ------------------------- #
@autheticatedfor_adminonly
def ShowCategory(request):
    category=Categories.objects.all()
    return render(request,'Admin/showCategory.html',{'category':category})

# ----------------------- Editing the category details ----------------------- #
@autheticatedfor_adminonly
def EditCategory(request, id):
    category=Categories.objects.get(id=id)
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        category.title=title
        category.description=description
        if category.title =='' or category.description =='' :
                messages.error(request, "Category fields cannot be blank")
                print('Field blank')
                return redirect(AddCategory)
        category.save()
        messages.success(request, 'Category is   Updated Successfully')
        return redirect(ShowCategory)
    return render(request, 'Admin/editCategory.html', {'category': category})

# --------------------------- Deleting the category -------------------------- #
def DeleteCategory(request,id):
    category=Categories.objects.get(id=id)
    category.delete()
    messages.success(request,"Category is deleted succesfully")
    return redirect(ShowCategory)

# ---------------------------------------------------------------------------- #
# --------------------------- Adding a new Subcategory -------------------------- #
@autheticatedfor_adminonly
def AddSubCategory(request):
    CategoryObj=Categories.objects.all()
    if request.method == 'POST':
            
            category=Categories.objects.get(id=request.POST['category'])
            title = request.POST['title']
            Subcategory_Image=request.FILES['Subcategory_Image']
            description = request.POST['description']
            if SubCategories.objects.filter(title=title).exists():
                messages.error(request, "This Category already Exists")
                print('This Subcategory exits')
                return redirect(ShowCategory)
            

            if title =='' :
                messages.error(request, "SubCategory fields cannot be blank")
                print('Filed blank')
                return redirect(AddSubCategory)
        
        
            subcategory = SubCategories.objects.create(category=category,
                        title=title,Subcategory_Image=Subcategory_Image,description=description)
            subcategory.save()
            messages.success(request, 'SubCategory has been Created Succesfully')
            return redirect(ShowSubCategory)
    
    return render(request,'Admin/addSubCategory.html',{'category':CategoryObj})

# ------------------------- Showing Whole Subcategories ------------------------- #
@autheticatedfor_adminonly
def ShowSubCategory(request):
    subcategory=SubCategories.objects.all()
    return render(request,'Admin/showSubcategory.html',{'subcategory':subcategory})


# ----------------------- Editing the Subcategory details ----------------------- #
@autheticatedfor_adminonly
def EditSubCategory(request, id):
    category=Categories.objects.all()
    subcategory=SubCategories.objects.get(id=id)
    if request.method == 'POST':
        category=Categories.objects.get(id=request.POST['category'])
        title = request.POST['title']
        description = request.POST['description']
        Subcategory_Image=request.FILES['Subcategory_Image']
        subcategory.title=title
        subcategory.category=category
        subcategory.description=description
        subcategory.Subcategory_Image=Subcategory_Image
        if subcategory.title =='' or subcategory.description =='' :
                messages.error(request, "SubCategory fields cannot be blank")
                print('Filed blank')
                return redirect(AddSubCategory)
        subcategory.save()
        messages.success(request, 'SubCategory is   Updated Successfully')
        return redirect(ShowSubCategory)
    return render(request, 'Admin/editsubCategory.html', {'subcategory': subcategory,'category': category})

# --------------------------- Deleting the Subcategory -------------------------- #
def DeleteSubCategory(request,id):
    category=SubCategories.objects.get(id=id)
    category.delete()
    messages.success(request,"Subcategory is deleted  succesfully")
    return redirect(ShowSubCategory)    
# ---------------------------------------------------------------------------- #
# --------------------------- Adding a new Product -------------------------- #
@autheticatedfor_adminonly
def AddProducts(request):
    category=Categories.objects.all()
    subcategory=SubCategories.objects.all()
    if request.method == 'POST':
            # category_id=request.POST['category_id']
            cat_id=Categories.objects.get(id=request.POST['category'])
            subcat_id=SubCategories.objects.get(id=request.POST['subcategories'])

            print(cat_id.id)
            print(subcat_id.id)
            Product_image=request.FILES['Product_image']
            product_name = request.POST['product_name']
            description = request.POST['product_description']
            product_long_description= request.POST['product_long_description']
            price=request.POST['price']
            AddedProduct = Products.objects.create(category_id=cat_id.id,subcategories_id=subcat_id.id,
                        product_name=product_name,Product_image=Product_image, product_description=description,product_long_description=product_long_description,price=price)
            AddedProduct.save()
            messages.success(request, 'Product has been Added Succesfully')
            return redirect(ShowProducts)
    return render(request,'Admin/addproduct.html',{'category':category,'subcategory':subcategory})

# ------------------------- Showing Whole Products ------------------------- #
@autheticatedfor_adminonly
def ShowProducts(request):
     products=Products.objects.all()
     return render(request,'Admin/showproducts.html',{'products':products})
# ------------------------- Deleting the Product ------------------------- #
def DeleteProducts(request,id):
    product=Products.objects.get(id=id)
    product.delete()
    messages.success(request,"Product is deleted succesfully")
    return redirect(ShowProducts)   

# ----------------------- Editing the Product details ----------------------- #
@autheticatedfor_adminonly
def EditProduct(request, id):
    product=Products.objects.get(id=id)
    category=Categories.objects.all()
    subcategory=SubCategories.objects.all()
    if request.method == 'POST':
        cat_id=Categories.objects.get(id=request.POST['category'])
        subcat_id=SubCategories.objects.get(id=request.POST['subcategories'])
        product_name = request.POST['product_name']
        Product_image=request.FILES['Product_image']
        product_description = request.POST['product_description']
        product_long_description=request.POST['product_long_description']
        product.category=cat_id
        product.subcategories=subcat_id
        product.product_name=product_name
        product.product_description=product_description
        product.product_long_description=product_long_description
        product.Product_image=Product_image
        
        product.save()
        print('saved')
        messages.success(request, 'Product is   Updated Successfully')
        return redirect(ShowProducts)
    return render(request, 'Admin/editProduct.html', {'product': product,'category':category,'subcategory':subcategory})

# ---------------------------------------------------------------------------- #
#                           admin logout here. session is deleted                         #
# ---------------------------------------------------------------------------- #
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminlogout(request):
    if 'username' in request.session:
       request.session.flush()
    # auth.logout(request)
    return redirect(adminlogin)





    








 


