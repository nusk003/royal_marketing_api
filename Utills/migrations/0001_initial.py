# Generated by Django 2.1.5 on 2019-02-23 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HeroSlider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('startPrice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('link', models.CharField(max_length=300)),
                ('mainImage', models.ImageField(upload_to='SliderImages/')),
                ('vectorImage', models.ImageField(upload_to='SliderImages/')),
            ],
        ),
    ]
