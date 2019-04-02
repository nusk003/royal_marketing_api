from rest_framework import serializers
from Utills.models import HeroSlider

class HeroSliderSerializer (serializers.ModelSerializer):

    class Meta:
        model = HeroSlider
        fields = '__all__'