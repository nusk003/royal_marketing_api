# Generated by Django 2.1.5 on 2019-02-01 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0003_auto_20190122_0838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproducts',
            name='discountPrice',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
    ]