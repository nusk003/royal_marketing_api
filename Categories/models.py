from django.db import models

# Create your models here.

class Categories(models.Model):

    catId = models.AutoField(primary_key=True)
    catTitle = models.CharField(max_length = 20)
    catDesc = models.CharField(max_length = 500)
    deleteCat = models.BooleanField(default = False) 

class CategoriesImages(models.Model):

    catImgId = models.AutoField(primary_key = True)
    catId = models.ForeignKey(Categories,related_name="CatImages",on_delete=models.CASCADE)
    catImg = models.ImageField(height_field='height_field',width_field='width_field', upload_to = "BrandImages/")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    deleteImg = models.BooleanField(default = False)

class ProductCategories(models.Model):

    proCatId = models.AutoField(primary_key = True)
    proCatTitle = models.CharField(max_length = 50)
    proCatDesc = models.CharField(max_length = 500)
    catId = models.ForeignKey(Categories,on_delete=models.CASCADE,related_name="proCat")
    deleteProCat = models.BooleanField(default = False)


class ProductCategoriesImages(models.Model):

    proCatImgId = models.AutoField(primary_key = True)
    proCatId = models.ForeignKey(ProductCategories,on_delete=models.CASCADE,related_name="proCatImages")
    proCatImg = models.ImageField(height_field='height_field',width_field='width_field', upload_to = "BrandImages/")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    deleteImg = models.BooleanField(default = False)

class Brands (models.Model):

    brandId = models.AutoField(primary_key = True)
    brandTitle = models.CharField(max_length = 50)
    brandDesc = models.CharField(max_length = 500)
    deleteBrand = models.BooleanField(default = False)

class BrandImages (models.Model):

    brandImgId = models.AutoField(primary_key = True)
    brandId = models.ForeignKey(Brands,on_delete=models.CASCADE,related_name="brandImages")
    brandImg = models.ImageField(height_field='height_field',width_field='width_field', upload_to = "BrandImages/")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    deleteImg = models.BooleanField(default = False)



