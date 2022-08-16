from email.policy import default
from django.db import models
from django.urls import reverse

# Create your models here.

class Categories(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        # managing plurals and singular
        verbose_name        = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class SubCategories(models.Model):
    id=models.AutoField(primary_key=True)
    category=models.ForeignKey(Categories,related_name='Subcategory',on_delete=models.CASCADE,null=True)
    title=models.CharField(max_length=255,unique=True)
    # slug = models.SlugField(max_length=100, unique=True)
    Subcategory_Image = models.ImageField(upload_to="media/",default=True)
    description=models.TextField() 
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Subcategory'
        verbose_name_plural = 'Subcategories'

    # def get_url(self):
    #     return reverse('products_by_subcategory', args=[self.slug])

    def __str__(self):
        return self.title


class Products(models.Model):
    id=models.AutoField(primary_key=True)
    category=models.ForeignKey(Categories,on_delete=models.CASCADE,null=True,default="")
    subcategories=models.ForeignKey(SubCategories,on_delete=models.CASCADE,null=True,default="")
    product_name=models.CharField(max_length=255)
    Product_image          = models.ImageField(upload_to='Products_Image',default=True)
    # images_two      = models.ImageField(upload_to='Products_Image', null=True)
    # images_three    = models.ImageField(upload_to='Products_Image', null=True)
    price           = models.IntegerField()
    is_available    = models.BooleanField(default=True)

    product_description=models.TextField()
    product_long_description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product_name



