# Generated by Django 2.1.5 on 2019-01-28 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0007_auto_20190128_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='subject',
            field=models.CharField(default='Service', max_length=20),
            preserve_default=False,
        ),
    ]
