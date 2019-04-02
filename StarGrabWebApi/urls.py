from django.conf.urls import url, include
#from tests.models import CustomUser
from User.models import User
from User.views import adminLoginView
from rest_framework import serializers, viewsets, routers,permissions,response
from Categories.api.views import TopCategoriesList,BrandList,SearchBrandList,SearchCategoryList,SearchProCatList,CreateCategoryView,CreateProductCategoryView,CreateBrandView,PopularBrandsView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from User.api.views import AreaList,SendVerificationCode,ValidateOTP,UpdateName,GetProfile
from Products.api.views import VariantList,VariantValueList,ProductLists,ProductList,UploadImage,CreateVariantView,CreateVariantValueView,FeatureProductListView
#from phone_login.views import (GenerateOTP)
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication


# Serializers define the API representation.


    

 #ViewSets define the view behavior.


# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
#router.register(r'api/users', UserViewSet)
router.register(r'api/areazone', AreaList)
#router.register(r'api/variantlist/(?P<variant>.+)/$',VariantList.as_view())
router.register(r'api/productlist', ProductList)
router.register(r'uploadImage', UploadImage)
router.register(r'api/categories/create',CreateCategoryView)
router.register(r'api/productcategories/create',CreateProductCategoryView)
router.register(r'api/brands/create',CreateBrandView)
router.register(r'api/variants/create',CreateVariantView)
router.register(r'api/variant/value/create', CreateVariantValueView)




# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^admin/',admin.site.urls),
    url(r'^api/admin/login/$', adminLoginView.as_view()),
    url(r'^api/variantlist/$', VariantList.as_view()),
    url(r'api/variantvaluelist/$', VariantValueList.as_view()),
    url(r'api/categories/$',SearchCategoryList.as_view()),
    url(r'api/productcategories/$',SearchProCatList.as_view()),
    url(r'api/brands/$',SearchBrandList.as_view()),
    url(r'api/verification/send',SendVerificationCode.as_view()),
    url(r'api/verification/verify',ValidateOTP.as_view()),
   
    url(r'api/products/featureproducts/$',FeatureProductListView.as_view()),
    url(r'api/categories/',include('Categories.api.urls')),
    url(r'api/cart/',include('Cart.api.urls')),
    url(r'api/user/',include('User.api.urls')),
    url(r'api/product/',include('Products.api.urls')),
    url(r'api/orders/',include('Orders.api.urls')),
    url(r'api/utills/',include('Utills.api.urls')),
    
  
]


if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)