from rest_framework import serializers
from Categories.models import CategoriesImages , Categories ,ProductCategories,ProductCategoriesImages ,Brands,BrandImages
from django.conf import settings 

class CategoryImagesSerializer (serializers.ModelSerializer):

    class Meta:
        model = CategoriesImages
        fields = ('__all__')
        read_only_fields = ('catId',)

class ProductCategoryImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategoriesImages
        fields = ('__all__')
        read_only_fields = ('proCatId',)



class ProductCategorySerializer (serializers.ModelSerializer):

    class Meta:
        model = ProductCategories
        fields = ('proCatId','proCatTitle',)

class CategorySerializer (serializers.ModelSerializer):

    images = serializers.SerializerMethodField()
    class Meta:
        model = Categories
        fields = ('catId','catTitle','images',)

    def get_images(self,cat):

        try :
            images = CategoriesImages.objects.filter(catId = cat,deleteImg = False)
            imgArr = []
            for image in images:
                imgArr.append(getattr(settings,'CUSTOM_DOMAIN','http://localhost:8000/media/')+str(image.catImg))
            return imgArr
        except :
            return []

class CategoryListSerializer (serializers.ModelSerializer):

    proCats = serializers.SerializerMethodField()
    class Meta:
        model = Categories
        fields = ('catId','catTitle','proCats',)

    def get_proCats(self,cat):

        try :
            proCats = ProductCategories.objects.filter(catId = cat,deleteProCat = False)
            ser = ProductCategorySerializer(instance = proCats,many = True)
            return ser.data

        except :
            return []

class CategoryCreateSerializer (serializers.ModelSerializer):

    CatImages = CategoryImagesSerializer(many=True)

    class Meta:
        model = Categories
        fields = ('__all__')

    def create (self,validated_data):

        CatImages = validated_data.pop('CatImages')
        category = Categories.objects.create(**validated_data)

        for catImage in CatImages:
            CategoriesImages.objects.create(**catImage , catId=category)
        return category    

class BrandImagesSerializer (serializers.ModelSerializer):

    class Meta:
        model = BrandImages
        fields = ('__all__')
        read_only_fields = ('brandId',)

class BrandSerializer (serializers.ModelSerializer):

    brandImages = BrandImagesSerializer(many = True)

    class Meta:
        model = Brands
        fields = ('__all__')


class ProductCatCreateSerializer (serializers.ModelSerializer):

    proCatImages = ProductCategoryImagesSerializer(many =True)

    class Meta:
        model = ProductCategories
        fields = ('__all__')

    def create(self,validated_data):

        proCatImages = validated_data.pop('proCatImages')
        proCat = ProductCategories.objects.create(**validated_data)
        for proCatImage in proCatImages:
            ProductCategoriesImages.objects.create(**proCatImage,proCatId = proCat)
        return proCat

class BrandCreateSerializer (serializers.ModelSerializer):

    brandImages = BrandImagesSerializer(many=True)

    class Meta:
        model = Brands
        fields = ('__all__')

    def create(self,validated_data):

        brandImages = validated_data.pop('brandImages')
        brand = Brands.objects.create(**validated_data)
        for brandImage in brandImages:
            BrandImages.objects.create(**brandImage,brandId = brand)
        return brand

class PopularBrandSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    class Meta:
        model = Brands
        fields = ('image','title','pk')

    def get_image(self,brand):

        try:
            image = BrandImages.objects.filter(brandId = brand,deleteImg=False).first()
            return getattr(settings,'CUSTOM_DOMAIN','http://localhost:8000/media/')+str(image.brandImg)
        except:
            return ""

    def get_title (self,brand):

        return brand.brandTitle

    
