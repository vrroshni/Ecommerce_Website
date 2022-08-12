from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
# the function defined inside this will manage the whole usercreation and superusercreation 

class MyAccountManager(BaseUserManager):
    #to create/Register user
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an e-mail address')
        
        if not username:
            raise ValueError('User must have an Username')

        user = self.model(
            email       = self.normalize_email(email),
            username    = username,
            first_name  = first_name,
            last_name   = last_name
        )
        #password will be hashed in database
        user.set_password(password)
        user.save(using=self._db)
        return user

     #to create/Register superuser
    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email      = self.normalize_email(email),
            username   = username,
            password   = password,
            first_name = first_name,
            last_name  = last_name
        )
        user.is_admin   = True
        user.is_active  = True
        user.is_staff   = True
        print("hello")
        user.is_superadmin  = True
        user.save(using=self._db)
        return user



#Using AbstractBaseUser,build from scratch
#Changes is not possible after making first makemigrations
class Account(AbstractBaseUser):
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(max_length=100, unique=True)
    phone_number    = models.CharField(max_length=50)
    referral_code   = models.CharField(max_length=50, null=True, blank=True)
    ref_active      = models.BooleanField(default=False ,null = True)
    code_reffered   = models.CharField(max_length=50, null=True, blank=True)
 

    #Required fields

    date_joined     = models.DateTimeField(auto_now_add=True)  
    last_login      = models.DateTimeField(auto_now_add=True)  
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_superadmin   = models.BooleanField(default=False)


   


    '''username will be a credential to login,
    we cant change it by providing email field instead of username and then add username in required fields and remove email the same'''

    USERNAME_FIELD      = 'username'
    REQUIRED_FIELDS     = ['email', 'first_name', 'last_name']

    objects = MyAccountManager()


    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


