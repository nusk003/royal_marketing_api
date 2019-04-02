from django.conf.urls import url, include
from .views import CreateOrder

urlpatterns = [
    url(r'create/$',CreateOrder.as_view()),
    
]