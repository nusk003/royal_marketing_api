from rest_framework.generics import ListAPIView
from Utills.api.serializers import HeroSliderSerializer
from Utills.models import HeroSlider
from rest_framework.permissions import AllowAny

class GetHeroSliderView (ListAPIView):

    queryset = HeroSlider.objects.all()
    serializer_class = HeroSliderSerializer
    permission_classes = (AllowAny,)
