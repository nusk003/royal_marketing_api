# Generated by Django 2.1.3 on 2019-01-14 15:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0008_auto_20190114_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verification',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime.now, editable=False),
        ),
    ]
