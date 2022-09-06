from email import message
from hmac import new
from itertools import count
from multiprocessing import context
from turtle import title
from unicodedata import category
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.models import auth,User
from Accounts.models import *
from .models import *
from django.views.decorators.cache import cache_control
from .decorators import*
from Order.models import *
from Cart.models import *
from django.core.paginator import Paginator
from django.db.models.functions import ExtractMonth,ExtractYear,ExtractDay
from django.db.models import Max,Min,Count,Avg,Sum
from django.contrib.auth.decorators import login_required
import calendar
from datetime import date
import datetime




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
                return redirect(adminDashboard)
            else :
                messages.error(request,'You are not authenticated to view coming pages')
        else:
                messages.error(request, '*Invalid Username or Password')
                return redirect(adminlogin)
       
    return render(request,'Admin/adminlogin.html')




# ------------------------------ Admin Dashboard ----------------------------- #
@login_required(login_url='Adminlogin')
@autheticatedfor_adminonly
def adminDashboard(request):
    orders=Order.objects.annotate(month=ExtractMonth('date')).values('month').annotate(count=Count('id')).values('month','count')
    yearorders=Order.objects.annotate(year=ExtractYear('date')).values('year').annotate(count=Count('id')).values('year','count')
    Dayorders=Order.objects.annotate(day=ExtractDay('date')).filter(date=date.today()).values('day').annotate(count=Count('id')).values('day','count')
    print(Dayorders)
    DayNumber=[]
    YearNumber=[]
    monthNumber=[]
    totalOrders=[]
    totaltyearorders=[]
    totaldayorder=[]
    for d in orders:
        monthNumber.append(calendar.month_name[d['month']])
        totalOrders.append(d['count'])
    for d in yearorders:
        YearNumber.append([d['year']])
        totaltyearorders.append(d['count']) 
    for d in Dayorders:
        DayNumber.append([d['day']])
        totaldayorder.append(d['count'])

# ---------------------------------- payment --------------------------------- #
    cod = Payment.objects.filter(payment_method = 'cashondelivery').aggregate(Count('id')).get('id__count')
    raz = Payment.objects.filter(payment_method = 'razorpay').aggregate(Count('id')).get('id__count')
    pay = Payment.objects.filter(payment_method = 'paypal').aggregate(Count('id')).get('id__count')
    context={
        'Order':orders,
        'MonthNumber':monthNumber,
        'TotalOrders':totalOrders,
        'YearNumber':YearNumber,
        'totaltyearorders':totaltyearorders,
        'DayNumber':DayNumber,
        'totaldayorder':totaldayorder,
        'paypal':pay,
        'raz':raz,
        'cod':cod
    }
    return render(request,'Admin/dashboard.html',context)



# ------------------------------- Sales Report ------------------------------- #

def salesReport(request):
    salesreport = Order.objects.filter(is_ordered = True).order_by('-id')
    context = {
            'salesreport':salesreport
            }

    return render(request,'Admin/salesreport.html',context)


def monthly_report(request,date):
    frmdate = date
    fm = [2022, frmdate, 1]
    todt = [2022,frmdate,28]
    salesreport = Order.objects.filter(date__gte = datetime.date(fm[0],fm[1],fm[2]),date__lte=datetime.date(todt[0],todt[1],todt[2]),is_ordered =True).order_by("-id")
    if len(salesreport)>0:
        context = {
            'salesreport':salesreport,
        }
        return render(request,'Admin/salesreport.html',context)
    else:
        messages.error(request,"No Orders")
        return render(request,'Admin/salesreport.html')



def yearly_report(request,date):
    frmdate = date
    fm = [frmdate, 1, 1]
    todt = [frmdate,12,31]
    salesreport = Order.objects.filter(date__gte = datetime.date(fm[0],fm[1],fm[2]),date__lte=datetime.date(todt[0],todt[1],todt[2]),is_ordered =True).order_by("-id")
    if len(salesreport)>0:
        context = {
            'salesreport':salesreport,
        }
        return render(request,'Admin/salesreport.html',context)
    else:
        messages.error(request,"No Orders")
        return render(request,'Admin/salesreport.html')

def date_range(request):
    if request.method == "POST":
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        if len(fromdate)>0 and len(todate)> 0 :
            frm = fromdate.split("-")
            tod = todate.split("-")
            fm = [int(x) for x in frm]
            todt = [int(x) for x in tod]
            salesreport = Order.objects.filter(date__gte = datetime.date(fm[0],fm[1],fm[2]),date__lte=datetime.date(todt[0],todt[1],todt[2]) ,is_ordered =True)
            context = {
                'salesreport':salesreport,
            }
            return render(request,'Admin/salesreport.html',context)
        else:
            salesreport = Order.objects.all()
            context = {
                'salesreport': salesreport ,
             }
    return render (request,"Admin/salesreport.html",context)
        




# ------------------- users data will be seen in this page ------------------- #
@login_required(login_url='Adminlogin')
@autheticatedfor_adminonly
def userdata(request):
    data = Account.objects.all().order_by('id')
    paginator=Paginator(data,per_page=3)
    page_number=request.GET.get('page')
    datafinal=paginator.get_page(page_number)
    totalpage=datafinal.paginator.num_pages
    context={
        'datas': datafinal,
        'lastpage':totalpage,
        'totalPagelist':[ n+1 for n  in range(totalpage)]
    }
    return render(request, 'Admin/adminuserdata.html',context)  

# --------------------------- for blocking User --------------------------- #
def BlockUser(request, id):
    print("entering")
    if request.method=='POST':

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
@login_required(login_url='Adminlogin')
@autheticatedfor_adminonly
def AddCategory(request):
    if request.method == 'POST':
            title = request.POST['title']
            description = request.POST['description']
            if Categories.objects.filter(title__icontains=title).exists():
                messages.error(request, "This Category  already Exists")
                print('This category exits')
                return redirect(ShowCategory)
     
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
@login_required(login_url='Adminlogin')
@autheticatedfor_adminonly
def ShowCategory(request):
    category=Categories.objects.all()
    paginator=Paginator(category,per_page=3)
    page_number=request.GET.get('page')
    categoryfinal=paginator.get_page(page_number)
    totalpage=categoryfinal.paginator.num_pages
    context={
        'category':categoryfinal,
        'lastpage':totalpage,
        'totalPagelist':[ n+1 for n  in range(totalpage)]

    }

    return render(request,'Admin/showCategory.html',context)

# ----------------------- Editing the category details ----------------------- #
@login_required(login_url='Adminlogin')
@autheticatedfor_adminonly
def EditCategory(request, id):
    category=Categories.objects.get(id=id)
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        category.title=title
        category.description=description
        if Categories.objects.exclude(id=id).filter(title__icontains=title).exists():
                messages.error(request, "SubCategory Already Exists")
                return redirect(AddCategory)
        if category.title =='' or category.description =='' :
                messages.error(request, "Category fields cannot be blank")
                print('Field blank')
                return redirect(AddCategory)
        category.save()
        messages.success(request, 'Category is   Updated Successfully')
        return redirect(ShowCategory)
    return render(request, 'Admin/editCategory.html', {'category': category})


# --------------------------- Deleting the category -------------------------- #
@login_required(login_url='Adminlogin')
@autheticatedfor_adminonly
def DeleteCategory(request,id):
    category=Categories.objects.get(id=id)
    category.delete()
    messages.success(request,"Category is deleted succesfully")
    return redirect(ShowCategory)

# ---------------------------------------------------------------------------- #


# ------------------------------ Category Offer ------------------------------ #
# --------------------------- Adding category offer -------------------------- #
@login_required(login_url='Adminlogin')
@autheticatedfor_adminonly
def New_CategoryOffer(request):
    CategoryObj=Categories.objects.all()
    if request.method=="POST":
        discount=request.POST.get("discount")
        category=request.POST.get("category_name")
        discount=int(discount)
        if Categoryoffer.objects.filter(category=category).exists():
            print("already exists")
            messages.info(request,"Offer already exists for this Category")
            return redirect(View_CategoryOffers)
        if discount>0:
            if discount<90:
                newCategoryOffer=Categoryoffer()
                newCategoryOffer.discount=discount
                newCategoryOffer.category=Categories.objects.get(id=category)
                newCategoryOffer.save()
                return redirect(View_CategoryOffers)
            else:
                messages.error(request,"Discount must be less than 90%")
                return redirect(New_CategoryOffer)
        else:
                messages.error(request,"Discount must be greater than 0%")
                return redirect(New_CategoryOffer)
    return render(request,'Offers/Add_NewCategoryOffer.html',{'Category':CategoryObj})

# ---------------------------- Edit CategoryOffer ---------------------------- #
@login_required(login_url='Adminlogin')
@autheticatedfor_adminonly
def Edit_CategoryOffer(request,id):
    CategoryObj=Categories.objects.all()
    CategoryOfferObj=Categoryoffer.objects.get(id=id)
    if request.method=="POST":
        discount=request.POST.get("discount")
        category=request.POST.get("category_name")
        discount=int(discount)
        if discount>0:
            if discount<90:
                CategoryOfferObj.discount=discount
                CategoryOfferObj.category=Categories.objects.get(id=category)
                CategoryOfferObj.save()
                return redirect(View_CategoryOffers)
            else:
                messages.error(request,"Discount must be less than 90%")
                return redirect(New_CategoryOffer)
        else:
                messages.error(request,"Discount must be greater than 0%")
                return redirect(New_CategoryOffer)
    context={
        'Category':CategoryObj,
        'CategoryOffer':CategoryOfferObj
    }
    return render(request,'Offers/Edit_CategoryOffer.html',context)



# --------------------------- View category Offers --------------------------- #
def View_CategoryOffers(request):
    CategoryOfferObj=Categoryoffer.objects.all()
    paginator=Paginator(CategoryOfferObj,per_page=2)
    page_number=request.GET.get('page')
    CategoryOfferObjfinal=paginator.get_page(page_number)
    totalpage=CategoryOfferObjfinal.paginator.num_pages
    context={
        'CategoryOffer':CategoryOfferObjfinal,
        'lastpage':totalpage,
        'totalPagelist':[ n+1 for n  in range(totalpage)]

    }
    return render(request,'Offers/View_CategoryOffer.html',context)

# -------------------------- Delete A Category Offer ------------------------- #
def Delete_CategoryOffer(request,id):
    toDelete_CategoryOffer=Categoryoffer.objects.get(id=id)
    toDelete_CategoryOffer.delete()
    messages.success(request,'Offer Deleted successfully')
    return redirect(View_CategoryOffers)

# ---------------------------- Block CategoryOffer --------------------------- #
def Block_CategoryOffer(request,id):
    toBlock_CategoryOffer=Categoryoffer.objects.get(id=id)
    toBlock_CategoryOffer.is_active=False
    toBlock_CategoryOffer.save()
    messages.error(request, 'Offer is Blocked Successfully')
    return redirect(View_CategoryOffers)

# --------------------------- Unblock CategoryOffer -------------------------- #
def UnBlock_CategoryOffer(request,id):
    toUnBlock_CategoryOffer=Categoryoffer.objects.get(id=id)
    toUnBlock_CategoryOffer.is_active=True
    toUnBlock_CategoryOffer.save()
    messages.error(request, 'Offer is UnBlocked Successfully')
    return redirect(View_CategoryOffers)





# --------------------------- Adding a new Subcategory -------------------------- #
@login_required(login_url='Adminlogin')
@autheticatedfor_adminonly
def AddSubCategory(request):
    CategoryObj=Categories.objects.all()
    if request.method == 'POST':
            
            category=Categories.objects.get(id=request.POST['category'])
            title = request.POST['title']
            Subcategory_Image=request.FILES['Subcategory_Image']
            description = request.POST['description']
            if SubCategories.objects.filter(title__icontains=title).exists():
                messages.error(request, "This Subcategory  already Exists")
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
@login_required(login_url='Adminlogin')
@autheticatedfor_adminonly
def ShowSubCategory(request):
    subcategory=SubCategories.objects.all()
    paginator=Paginator(subcategory,per_page=2)
    page_number=request.GET.get('page')
    subcategoryfinal=paginator.get_page(page_number)
    totalpage=subcategoryfinal.paginator.num_pages
    context={
        'subcategory':subcategoryfinal,
        'lastpage':totalpage,
        'totalPagelist':[ n+1 for n  in range(totalpage)]

    }

    return render(request,'Admin/showSubcategory.html',context)


# ----------------------- Editing the Subcategory details ----------------------- #
@login_required(login_url='Adminlogin')
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
        if SubCategories.objects.exclude(id=id).filter(title__icontains=title).exists():
                messages.error(request, "SubCategory Already Exists")
                return redirect(AddSubCategory)

        

        if subcategory.title =='' or subcategory.description =='' :
                messages.error(request, "SubCategory fields cannot be blank")
                print('Field blank')
                return redirect(AddSubCategory)
        subcategory.save()
        messages.success(request, 'SubCategory is   Updated Successfully')
        return redirect(ShowSubCategory)
    return render(request, 'Admin/editsubCategory.html', {'subcategory': subcategory,'category': category})

# --------------------------- Deleting the Subcategory -------------------------- #
@login_required(login_url='Adminlogin')
@autheticatedfor_adminonly
def DeleteSubCategory(request,id):
    subcategory=SubCategories.objects.get(id=id)
    subcategory.delete()
    messages.success(request,"Subcategory is deleted  succesfully")
    return redirect(ShowSubCategory)

# ------------------------------ SubCategory Offer ------------------------------ #
@login_required(login_url='Adminlogin')
@autheticatedfor_adminonly
def New_SubCategoryOffer(request):
    SubCategoryObj=SubCategories.objects.all()
    if request.method=="POST":
        discount=request.POST.get("discount")
        subcategory=request.POST.get("subcategory_name")
        discount=int(discount)
        if SubCategoryoffer.objects.filter(subcategory=subcategory).exists():
            print("already exists")
            messages.info(request,"Offer already exists for this SubCategory")
            return redirect(View_SubCategoryOffers)
        
        if discount>0:
            if discount<90:
                newSubCategoryOffer=SubCategoryoffer()
                newSubCategoryOffer.subcategory=SubCategories.objects.get(id=subcategory)
                newSubCategoryOffer.discount=discount
                newSubCategoryOffer.save()
                
                return redirect(View_SubCategoryOffers)
            else:
                messages.error(request,"Discount must be less than 90%")
                return redirect(New_SubCategoryOffer)
        else:
                messages.error(request,"Discount must be greater than 0%")
                return redirect(New_SubCategoryOffer)
    context={
       
        'SubCategory':SubCategoryObj,

    }
    return render(request,'Offers/Add_NewSubCategoryOffer.html',context)   


# ---------------------------- Edit SubCategoryOffer ---------------------------- #
@login_required(login_url='Adminlogin')
@autheticatedfor_adminonly
def Edit_SubCategoryOffer(request,id):
    SubCategoryObj=SubCategories.objects.all()
    SubCategoryOfferObj=SubCategoryoffer.objects.get(id=id)
    if request.method=="POST":
        discount=request.POST.get("discount")
        subcategory=request.POST.get("subcategory_name")

        discount=int(discount)
        if discount>0:
            if discount<90:
                SubCategoryOfferObj.discount=discount
                SubCategoryOfferObj.subcategory=SubCategories.objects.get(id=subcategory)
                SubCategoryOfferObj.save()
                return redirect(New_SubCategoryOffer)
            else:
                messages.error(request,"Discount must be less than 90%")
                return redirect(Edit_SubCategoryOffer)
        else:
                messages.error(request,"Discount must be greater than 0%")
                return redirect(Edit_SubCategoryOffer)
    context={
        'Subcategory':SubCategoryObj,
        'SubCategoryOffer':SubCategoryOfferObj
    }
    return render(request,'Offers/Edit_SubCategoryOffer.html',context) 
# --------------------------- View Subcategory Offers --------------------------- #
def View_SubCategoryOffers(request):
    SubCategoryOfferObj=SubCategoryoffer.objects.all().order_by('id')
    paginator=Paginator(SubCategoryOfferObj,per_page=2)
    page_number=request.GET.get('page')
    SubCategoryOfferObjfinal=paginator.get_page(page_number)
    totalpage=SubCategoryOfferObjfinal.paginator.num_pages
    context={
        'SubCategoryOffer':SubCategoryOfferObjfinal,
        'lastpage':totalpage,
        'totalPagelist':[ n+1 for n  in range(totalpage)]

    }
    return render(request,'Offers/View_SubCategoryOffer.html',context)
# -------------------------- Delete SubCategoryOffer ------------------------- #
def Delete_SubCategoryOffer(request,id):
    toDelete_SubCategoryOffer=SubCategoryoffer.objects.get(id=id)
    toDelete_SubCategoryOffer.delete()
    messages.success(request,'Offer Deleted successfully')
    return redirect(View_SubCategoryOffers)

# ---------------------------- Block SubCategoryOffer --------------------------- #
def Block_SubCategoryOffer(request,id):
    toBlock_SubCategoryOffer=SubCategoryoffer.objects.get(id=id)
    toBlock_SubCategoryOffer.is_active=False
    toBlock_SubCategoryOffer.save()
    messages.error(request, 'Offer is Blocked Successfully')
    return redirect(View_SubCategoryOffers)

# --------------------------- Unblock SubCategoryOffer -------------------------- #
def UnBlock_SubCategoryOffer(request,id):
    toUnBlock_SubCategoryOffer=SubCategoryoffer.objects.get(id=id)
    toUnBlock_SubCategoryOffer.is_active=True
    toUnBlock_SubCategoryOffer.save()
    messages.error(request, 'Offer is UnBlocked Successfully')
    return redirect(View_SubCategoryOffers)



# --------------------------- Adding a new Product -------------------------- #
@login_required(login_url='Adminlogin')
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
            Productimage_two=request.FILES['Productimage_two']
            Productimage_three=request.FILES['Productimage_three']
            product_name = request.POST['product_name']
            description = request.POST['product_description']
            product_long_description= request.POST['product_long_description']
            price=request.POST['price']
            stock=request.POST['stock']
            if Products.objects.filter(product_name__icontains=product_name).exists():
                messages.error(request, "This Product  already Exists")
                print('This Product exists')
                return redirect(ShowProducts)
            if product_name =='' or description=='' :
                messages.error(request, " fields cannot be blank")
                print('Field blank')
                return redirect(AddProducts)
            AddedProduct = Products.objects.create(category_id=cat_id.id,subcategories_id=subcat_id.id,
                        product_name=product_name,Product_image=Product_image,Productimage_two=Productimage_two,Productimage_three=Productimage_three, product_description=description,product_long_description=product_long_description,price=price,stock=stock)
            AddedProduct.save()
            messages.success(request, 'Product has been Added Succesfully')
            return redirect(ShowProducts)
    return render(request,'Admin/addproduct.html',{'category':category,'subcategory':subcategory})

# ------------------------- Showing Whole Products ------------------------- #
@login_required(login_url='Adminlogin')
@autheticatedfor_adminonly
def ShowProducts(request):
     products=Products.objects.all()
     paginator=Paginator(products,per_page=3)
     page_number=request.GET.get('page')
     productsfinal=paginator.get_page(page_number)
     totalpage=productsfinal.paginator.num_pages
     context={
        'products':productsfinal,
        'lastpage':totalpage,
        'totalPagelist':[ n+1 for n  in range(totalpage)]

    }
     return render(request,'Admin/showproducts.html',context)
# ------------------------- Deleting the Product ------------------------- #
@login_required(login_url='Adminlogin')
@autheticatedfor_adminonly
def DeleteProducts(request,id):
    product=Products.objects.get(id=id)
    product.delete()
    messages.success(request,"Product is deleted succesfully")
    return redirect(ShowProducts)   

# ----------------------- Editing the Product details ----------------------- #
@login_required(login_url='Adminlogin')
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
        Productimage_two=request.FILES['Productimage_two']
        Productimage_three=request.FILES['Productimage_three']
        product_description = request.POST['product_description']
        product_long_description=request.POST['product_long_description']
        if Products.objects.exclude(id=id).filter(product_name__icontains=product_name).exists():
                messages.error(request, "Product Already Exists")
                return redirect(ShowProducts)
        if product_name =='' or product_description=='' :
                messages.error(request, " fields cannot be blank")
                print('Field blank')
                return redirect(AddProducts)
        product.category=cat_id
        product.subcategories=subcat_id
        product.product_name=product_name
        product.product_description=product_description
        product.product_long_description=product_long_description
        product.Product_image=Product_image
        product.Productimage_two=Productimage_two
        product.Productimage_three=Productimage_three
        
        product.save()
        print('saved')
        messages.success(request, 'Product is   Updated Successfully')
        return redirect(ShowProducts)
    return render(request, 'Admin/editProduct.html', {'product': product,'category':category,'subcategory':subcategory})


# ------------------------------ Product Offer ------------------------------ #
# --------------------------- Adding Product  offer -------------------------- #
@login_required(login_url='Adminlogin')
@autheticatedfor_adminonly
def New_ProductOffer(request):
    products=Products.objects.all()
    if request.method=="POST":
        discount=request.POST.get("discount")
        choosed_product=request.POST.get("product_name")
        if Productoffer.objects.filter(product=choosed_product).exists():
            print("already exists")
            messages.info(request,"Offer already exists for this Product")
            return redirect(View_ProductOffers)
        discount=int(discount)
        if discount>0:
            if discount<90:
                newProductOffer=Productoffer()
                newProductOffer.discount=discount
                newProductOffer.product=Products.objects.get(id=choosed_product)
                newProductOffer.save()
                return redirect(View_ProductOffers)
            else:
                messages.error(request,"Discount must be less than 90%")
                return redirect(New_ProductOffer)
        else:
                messages.error(request,"Discount must be greater than 0%")
                return redirect(New_ProductOffer)
    return render(request,'Offers/Add_NewProductOffer.html',{'Products':products})

# # ---------------------------- Edit ProductOffer ---------------------------- #
@login_required(login_url='Adminlogin')
@autheticatedfor_adminonly
def Edit_ProductOffer(request,id):
    products=Products.objects.all()
    ProductOfferObj=Productoffer.objects.get(id=id)
    if request.method=="POST":
        discount=request.POST.get("discount")
        choosed_product=request.POST.get("product_name")
        discount=int(discount)
        if discount>0:
            if discount<90:
                ProductOfferObj.discount=discount
                ProductOfferObj.category=Products.objects.get(id=choosed_product)
                ProductOfferObj.save()
                return redirect(View_ProductOffers)
            else:
                messages.error(request,"Discount must be less than 90%")
                return redirect(Edit_ProductOffer)
        else:
                messages.error(request,"Discount must be greater than 0%")
                return redirect(Edit_ProductOffer)
    context={
        'Products':products,
        'ProductOfferObj':ProductOfferObj
    }
    return render(request,'Offers/Edit_ProductOffer.html',context)



# # --------------------------- View Product Offers --------------------------- #
def View_ProductOffers(request):
    ProductOfferObj=Productoffer.objects.all()
    paginator=Paginator(ProductOfferObj,per_page=2)
    page_number=request.GET.get('page')
    ProductOfferObjfinal=paginator.get_page(page_number)
    totalpage=ProductOfferObjfinal.paginator.num_pages
    context={
        'ProductOffer':ProductOfferObjfinal,
        'lastpage':totalpage,
        'totalPagelist':[ n+1 for n  in range(totalpage)]

    }
    return render(request,'Offers/View_ProductOffer.html',context)


# -------------------------- Delete A Product Offer ------------------------- #
def Delete_ProductOffer(request,id):
    toDelete_ProductOffer=Productoffer.objects.get(id=id)
    toDelete_ProductOffer.delete()
    messages.success(request,'Offer Deleted successfully')
    return redirect(View_ProductOffers)

# ---------------------------- Block ProductOffer --------------------------- #
def Block_ProductOffer(request,id):
    toBlock_ProductOffer=Productoffer.objects.get(id=id)
    toBlock_ProductOffer.is_active=False
    toBlock_ProductOffer.save()
    messages.error(request, 'Offer is Blocked Successfully')
    return redirect(View_ProductOffers)

# --------------------------- Unblock ProductOffer -------------------------- #
def UnBlock_ProductOffer(request,id):
    toUnBlock_ProductOffer=Productoffer.objects.get(id=id)
    toUnBlock_ProductOffer.is_active=True
    toUnBlock_ProductOffer.save()
    messages.error(request, 'Offer is UnBlocked Successfully')
    return redirect(View_ProductOffers)


# ---------------------------------- coupon ---------------------------------- #
def add_coupons(request):
    coupons=Coupons.objects.all()
    if request.method=="POST":
        coupon=request.POST['code']
        valid_to=request.POST['validity']
        discount=request.POST['discount']
        coupon_code=Coupons.objects.create(coupon_code=coupon,valid_to=valid_to,discount=discount)

    return render(request,'Offers/Add_coupon.html',{'coupons':coupons})






@login_required(login_url='Adminlogin')
@autheticatedfor_adminonly
def Adminvieworder_Details(request):
   orderproductdetails=Order_Product.objects.all().order_by('id')
   paginator=Paginator(orderproductdetails,per_page=5)
   page_number=request.GET.get('page')
   orderproductdetailsFinal=paginator.get_page(page_number)
   totalpage=orderproductdetailsFinal.paginator.num_pages
   context={
        'OrderProductDetails':orderproductdetailsFinal,
        'lastpage':totalpage,
        'totalPagelist':[ n+1 for n  in range(totalpage)]

    }

   return render(request,'Admin/OrderList.html',context)  



def order_Cancelled(request,id):
    user=request.user
    orderproductdetails=Order_Product.objects.get(id=id)
    print(orderproductdetails.status)
    orderproductdetails.status='Cancelled'
    print('------------------')
    orderproductdetails.save()
    print(orderproductdetails.status)

    return redirect(Adminvieworder_Details)

def order_Shipped(request,id):
    user=request.user
    orderproductdetails=Order_Product.objects.get(id=id)
    print(orderproductdetails.status)
    orderproductdetails.status='Shipped'
    print('------------------')
    orderproductdetails.save()
    print(orderproductdetails.status)

    return redirect(Adminvieworder_Details)

def order_Out_For_delivery(request,id):
    user=request.user
    orderproductdetails=Order_Product.objects.get(id=id)
    print(orderproductdetails.status)
    orderproductdetails.status='Out for delivery'
    print('------------------')
    orderproductdetails.save()
    print(orderproductdetails.status)

    return redirect(Adminvieworder_Details)


def order_Delivered(request,id):
    user=request.user
    orderproductdetails=Order_Product.objects.get(id=id)
    print(orderproductdetails.status)
    orderproductdetails.status='Delivered'
    print('------------------')
    orderproductdetails.save()
    print(orderproductdetails.status)

    return redirect(Adminvieworder_Details)



# ---------------------------------------------------------------------------- #
#                           admin logout here. session is deleted              #
# ---------------------------------------------------------------------------- #
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminlogout(request):
    if 'username' in request.session:
       request.session.flush()
    # auth.logout(request)
    return redirect(adminlogin)





    








 



