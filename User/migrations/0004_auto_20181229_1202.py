# Generated by Django 2.1.3 on 2018-12-29 06:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_auto_20181229_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verification',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
