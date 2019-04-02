from django.conf.urls import url,include
from .views import GetProfile,MyOrdersView,UpdateName,EditAddress,DeleteAddress,AddAddress

urlpatterns = [
    url(r'profile',GetProfile.as_view()),
    url(r'orders',MyOrdersView.as_view()),
    url(r'updatename',UpdateName.as_view()),
    url(r'updateaddress',EditAddress.as_view()),
    url(r'deleteaddress',DeleteAddress.as_view()),
    url(r'createaddress',AddAddress.as_view()),

]
