from django.conf.urls import url, include
from .views import AddtoCartView,UpdateCartProView,GetCartView,DeleteCart,checkPromoCode,PromoCodeOffline,MergeCart

urlpatterns = [
    url(r'addtocart',AddtoCartView.as_view()),
    url(r'updatecart',UpdateCartProView.as_view()),
    url(r'getcart/$',GetCartView.as_view()),
    url(r'deletecart/',DeleteCart.as_view()),
    url(r'checkpromocode',checkPromoCode.as_view()),
    url(r'offlinepromocode',PromoCodeOffline.as_view()),
    url(r'mergecart/',MergeCart.as_view()),


]