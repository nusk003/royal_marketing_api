from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone
import datetime


# Create your models here.
class Area (models.Model):

    areaId = models.AutoField(primary_key = True)
    area = models.CharField(max_length = 20)
    latitude = models.DecimalField(max_digits=15,decimal_places=5,default=300.00)
    longitude = models.DecimalField(max_digits=15,decimal_places=5,default=300.00)
    areaImg = models.ImageField(height_field=None,width_field=None)
    deliverCharge = models.DecimalField(max_digits=6,decimal_places=2,default = 200.00)
    deleteArea = models.BooleanField(default=False)

class Royality (models.Model):

    royalityId = models.AutoField(primary_key = True)
    royality = models.CharField(max_length = 20)
    subscribeCharge = models.DecimalField(max_digits=6,decimal_places=2)
    royalityDesc = models.CharField(max_length = 200)
    isLive = models.BooleanField(default=True)
    deleteRoyality = models.BooleanField(default=False)

class MyUserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self,phone,email=None,password=None,is_customer = False,is_admin = False,is_staff = False,name =""):

        if not phone:
            raise ValueError("Users must have Phone No")


        user = self.model(
            email = self.normalize_email(email),
            phone=phone,
            name = name,
        )

        user.set_password(password)
        user.is_superuser = is_admin
        user.is_staff = is_staff
      #  user.name = name
       # user.phone = phone
        user.is_customer = is_customer
        
        user.save(using=self._db)
        return user

    def create_superuser(self,email,phone,password,name):

        user = self.create_user(
            email = email,
            phone = phone,
            password=password,
            is_admin=True,
            is_staff=True,
            name = name
        )

        user.save(using=self._db)
        return user

class User (AbstractBaseUser):

    name = models.CharField(max_length = 20)
    phone = PhoneNumberField(unique = True)
   # userType = models.ForeignKey(UserType,on_delete=models.CASCADE,related_name="Users")
    area = models.ForeignKey(Area,on_delete=models.CASCADE,related_name="Users",null=True,blank=True)
   # username = models.CharField(max_length=20)
    dateOfJoin = models.DateTimeField(auto_now=True)
    isRoyality = models.BooleanField(default=False)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default = True)
    is_staff = models.BooleanField(default= True)
    is_customer = models.BooleanField(default = False)
    is_vendor = models.BooleanField(default=False)
 #   is_staff = models.BooleanField(default = True)
    royalityId = models.ForeignKey(Royality,on_delete = models.CASCADE,related_name="Customers",blank = True,null =True)
    

    

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email','name']

    objects = MyUserManager()

    def get_full_name(self):

        return self.name
    
    def get_short_name(self):

        return self.name

    def __str__(self):

        return self.email

    
   
    def has_perm(self, perm, obj=None):
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # Simplest possible answer: Yes, always
        return True

class Verification(models.Model):

    verificationId = models.AutoField(primary_key = True)
    phone = PhoneNumberField(editable = False)
    otp = models.CharField(max_length=10, editable=False)
    timestamp = models.DateTimeField(editable=False,default=datetime.datetime.now)
    attempts = models.IntegerField(default=0)
    used = models.BooleanField(default=False)
    

class UserAddress (models.Model):

    userAddressId = models.AutoField(primary_key = True)
    userId = models.ForeignKey(User,on_delete=models.CASCADE,related_name="Address")
    address = models.CharField(max_length = 50)
    latitude = models.DecimalField(max_digits=15,decimal_places=5,default=300.00)
    longitude = models.DecimalField(max_digits=15,decimal_places=5,default=400.00)
    deleteAddress = models.BooleanField(default=False)

class PromoCodes (models.Model):

    promoCodeId = models.AutoField(primary_key = True)
    promoCode = models.CharField(max_length = 20)
    discountType = models.IntegerField()
    discountValue = models.DecimalField(max_digits=5,decimal_places=2)
    startDate = models.DateTimeField(auto_now=True)
    endDate = models.DateTimeField(auto_now=False)
    minPrice = models.DecimalField(max_digits=10,decimal_places=2)
    maxPrice = models.DecimalField(max_digits=10,decimal_places=2)
    isForAll = models.BooleanField(default=False)
    isLive = models.BooleanField(default=True)
    delete = models.BooleanField(default=False)

class CustomerPromoCodes(models.Model):

    customerPromoCodeId = models.AutoField(primary_key = True)
    customerId = models.ForeignKey(User,on_delete=models.CASCADE,related_name="PromoCodes")
    promoCodeId = models.ForeignKey(PromoCodes,on_delete=models.CASCADE,related_name="Customers")
    deleteCustomerPromocode = models.BooleanField(default=False)
    isLive = models.BooleanField(default=True)
    isUsed =models.BooleanField(default=False)

class UsedPromoCodes (models.Model):

    usedPromoCodeId = models.AutoField(primary_key = True)
    promoCodeId = models.ForeignKey(PromoCodes,on_delete=models.CASCADE,related_name="UsedCustomers")
    customerId = models.ForeignKey(User,on_delete=models.CASCADE,related_name="UsedPromoCodes")

class CashBack (models.Model):

    cashBackId = models.AutoField(primary_key = True)
    customerId = models.ForeignKey(User,on_delete=models.CASCADE,related_name="CashBacks")
    amount = models.DecimalField(max_digits=7,decimal_places=2)
    startDate = models.DateTimeField(auto_now=True)
    endDate = models.DateTimeField()
    isUsed = models.BooleanField(default=False)
    isLive = models.BooleanField(default=True)
    deleteCashBack = models.BooleanField(default=False)


  


