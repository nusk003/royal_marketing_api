# Generated by Django 2.1.5 on 2019-01-28 07:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Products', '0005_auto_20190117_1839'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Reviews', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
