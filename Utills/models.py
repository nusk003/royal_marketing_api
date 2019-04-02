from django.db import models

# Create your models here.
class HeroSlider (models.Model):

    title = models.CharField(max_length = 60)
    startPrice = models.DecimalField(max_digits=10,decimal_places=2)
    link = models.CharField(max_length = 300)
    mainImage = models.ImageField(upload_to = "SliderImages/")
    vectorImage = models.ImageField(upload_to = "SliderImages/")
