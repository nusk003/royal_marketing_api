from django.conf.urls import url, include
from Utills.api.views import GetHeroSliderView

urlpatterns = [
    url(r'getheroslider/',GetHeroSliderView.as_view())
]