from django.db import models
from Categories.models import Categories,Brands,ProductCategories
from User.models import User
import datetime


# Create your models here.


class Products (models.Model):

    id = models.AutoField(primary_key = True)
    productTitle = models.CharField(max_length = 50)
    productDesc = models.CharField(max_length = 1000)
    catId = models.ForeignKey(Categories,on_delete=models.CASCADE,related_name="products")
    brandId = models.ForeignKey(Brands,on_delete=models.CASCADE,related_name="products")
    proCatId = models.ForeignKey(ProductCategories,on_delete=models.CASCADE,related_name="products")
    hasVariants = models.BooleanField(default=False)
    dateOfAdded = models.DateTimeField(auto_now=True)
    deletePro = models.BooleanField(default=False)
    isLive = models.BooleanField(default=True)


    def currentVendor (self):
        return ProductVendor.objects.filter(product=self,vendorId=4).order_by('sellPrice')
    
class Variants (models.Model):

    varId = models.AutoField(primary_key = True)
    variantTitle = models.CharField(max_length = 20)
    deleteVariant = models.BooleanField(default=False)

 

class VariantValues (models.Model):

    varValId = models.AutoField(primary_key = True)
    varId = models.ForeignKey(Variants,on_delete=models.CASCADE,related_name="VariantVal")
    varValue = models.CharField(max_length = 20)
    deleteVarValue = models.BooleanField(default=False)


class ProductCombinations (models.Model):

    combinationId = models.AutoField(primary_key = True)
    product = models.ForeignKey(Products,on_delete=models.CASCADE,related_name="Combinations")
    isLive = models.BooleanField(default = True)
    isStock = models.BooleanField(default = True)
    deleteComb = models.BooleanField(default = False)

class CombinationValues (models.Model):

    combValueId = models.AutoField(primary_key = True)
    proCombId = models.ForeignKey(ProductCombinations,on_delete = models.CASCADE,related_name="combValues")
    variantValue = models.ForeignKey(VariantValues,on_delete=models.CASCADE,related_name = "Variants")
    isLive = models.BooleanField(default=True)
    delete = models.BooleanField(default = False)

class ProductCombinationImages(models.Model):

    proVarImgId = models.AutoField(primary_key = True)
    proVarId = models.ForeignKey(ProductCombinations,on_delete=models.CASCADE,related_name="Images",blank=True,null=True)
    product = models.ForeignKey(Products,on_delete=models.CASCADE,related_name="Images")
    proVarImg = models.ImageField(width_field=None,height_field=None,upload_to = "ProductImages/" )
    deleteImg = models.BooleanField(default=False)
    
class ProductCombinationKeywords (models.Model):

    proKeyId = models.AutoField(primary_key = True)
    proVarId = models.ForeignKey(ProductCombinations,on_delete=models.CASCADE,related_name="Keywords",blank=True,null=True)
    product = models.ForeignKey(Products,on_delete=models.CASCADE,related_name="Keywords")
    keyword = models.CharField(max_length = 50)
    deleteKeyword = models.BooleanField(default=False)

class ProductVendor(models.Model):

    proVendorId = models.AutoField(primary_key = True)
    vendorId = models.ForeignKey(User,on_delete=models.CASCADE,related_name="Products")
    proVarId = models.ForeignKey(ProductCombinations,on_delete=models.CASCADE,related_name="prices",blank=True,null=True)
    product = models.ForeignKey(Products,on_delete=models.CASCADE,related_name="prices")
    costPrice = models.DecimalField(max_digits=7,decimal_places=2)
    sellPrice = models.DecimalField(max_digits=7,decimal_places=2)
    isStock = models.BooleanField(default=False)
    deleteProVendor = models.BooleanField(default=False)
    isLive = models.BooleanField(default=True)
    dateOfAdded = models.DateTimeField(auto_now=True)

class Offer(models.Model):

    offerId = models.AutoField(primary_key = True)
    offerTitle = models.CharField(max_length = 20)
    startDate = models.DateTimeField(editable=False,default=datetime.datetime.now)
    endDate = models.DateTimeField()
    deleteOffer = models.BooleanField(default=False)
    isLive = models.BooleanField(default=False)

   
    @property
    def is_valid (self):

        try:
            off = Offer.objects.get(offerId=self.offerId,endDate__gte = datetime.datetime.now(),startDate__lte = datetime.datetime.now(),isLive=True,deleteOffer = False)
            return True
        except:
            return False
            
        
    

class OfferProductVendors(models.Model):

    offerProductVendorId = models.AutoField(primary_key = True)
    proVendorId = models.ForeignKey(ProductVendor,on_delete=models.CASCADE,related_name="Offers")
    offerId =  models.ForeignKey(Offer,on_delete=models.CASCADE,related_name="Products")
    offerPrice = models.DecimalField(max_digits=10,decimal_places=2)
    deleteOfferPro = models.BooleanField(default=False)
    isLive = models.BooleanField(default=False)

class FreeOffer(models.Model):

    freeOfferId = models.AutoField(primary_key = True)
    offerName = models.CharField(max_length = 50)
    proVendorId = models.ForeignKey(ProductVendor,on_delete=models.CASCADE,related_name="FreeOffers")
    offerDesc = models.CharField(max_length = 500)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    deleteOffer = models.BooleanField(default=False)
    isLive =models.BooleanField(default=True)

class FreeProducts (models.Model):

    freeProductId = models.AutoField(primary_key = True)
    freeOfferId = models.ForeignKey(FreeOffer,on_delete=models.CASCADE,related_name="FreeProducts")
    freeProVendorId = models.ForeignKey(ProductVendor,on_delete=models.CASCADE,related_name="FreeProducts")
    deleteFreeProduct = models.BooleanField(default=False)
    isLive = models.BooleanField(default = True)

    
class RainCheck (models.Model):

    rainCheckId = models.AutoField(primary_key = True)
    customerId = models.ForeignKey(User,on_delete=models.CASCADE,related_name="RainChecks")
    productVendorId = models.ForeignKey(ProductVendor,on_delete=models.CASCADE,related_name="RainChecks")
    deleteRainCheck = models.BooleanField(default=False)

class Review (models.Model):

    reviewId = models.AutoField(primary_key = True)
    productId = models.ForeignKey(Products,on_delete=models.CASCADE,related_name="Reviews")
    customer = models.ForeignKey(User,on_delete=models.CASCADE,related_name="Reviews")
    subject = models.CharField(max_length = 20)
    stars = models.IntegerField()
    review = models.CharField(max_length = 500)
    deleteReview = models.BooleanField(default=False)
    isLive = models.BooleanField(default=True)
    
