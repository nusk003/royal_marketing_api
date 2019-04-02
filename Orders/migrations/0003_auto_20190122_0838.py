# Generated by Django 2.1.3 on 2019-01-22 03:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0005_auto_20190117_1839'),
        ('Orders', '0002_auto_20190122_0807'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproducts',
            name='offerProductVendorsId',
        ),
        migrations.AddField(
            model_name='orderproducts',
            name='offerProductVendorId',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='OrderProducts', to='Products.OfferProductVendors'),
        ),
    ]