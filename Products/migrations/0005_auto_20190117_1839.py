# Generated by Django 2.1.3 on 2019-01-17 13:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0004_offerproductvendors_offerprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='startDate',
            field=models.DateTimeField(default=datetime.datetime.now, editable=False),
        ),
    ]
