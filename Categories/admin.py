from django.contrib import admin
from .models import ( Categories,CategoriesImages,ProductCategories,ProductCategoriesImages,Brands,BrandImages)
# Register your models here.
admin.site.register(Categories)
admin.site.register(CategoriesImages)
admin.site.register(ProductCategories)
admin.site.register(ProductCategoriesImages)
admin.site.register(Brands)
admin.site.register(BrandImages)