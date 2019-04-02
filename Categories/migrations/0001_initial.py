# Generated by Django 2.1.3 on 2018-12-20 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BrandImages',
            fields=[
                ('brandImgId', models.AutoField(primary_key=True, serialize=False)),
                ('brandImg', models.ImageField(height_field='height_field', upload_to='BrandImages/', width_field='width_field')),
                ('height_field', models.IntegerField(default=0)),
                ('width_field', models.IntegerField(default=0)),
                ('deleteImg', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Brands',
            fields=[
                ('brandId', models.AutoField(primary_key=True, serialize=False)),
                ('brandTitle', models.CharField(max_length=50)),
                ('brandDesc', models.CharField(max_length=500)),
                ('deleteBrand', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('catId', models.AutoField(primary_key=True, serialize=False)),
                ('catTitle', models.CharField(max_length=20)),
                ('catDesc', models.CharField(max_length=500)),
                ('deleteCat', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CategoriesImages',
            fields=[
                ('catImgId', models.AutoField(primary_key=True, serialize=False)),
                ('catImg', models.ImageField(height_field='height_field', upload_to='BrandImages/', width_field='width_field')),
                ('height_field', models.IntegerField(default=0)),
                ('width_field', models.IntegerField(default=0)),
                ('deleteImg', models.BooleanField(default=False)),
                ('catId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CatImages', to='Categories.Categories')),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategories',
            fields=[
                ('proCatId', models.AutoField(primary_key=True, serialize=False)),
                ('proCatTitle', models.CharField(max_length=50)),
                ('proCatDesc', models.CharField(max_length=500)),
                ('deleteProCat', models.BooleanField(default=False)),
                ('catId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proCats', to='Categories.Categories')),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategoriesImages',
            fields=[
                ('proCatImgId', models.AutoField(primary_key=True, serialize=False)),
                ('proCatImg', models.ImageField(height_field='height_field', upload_to='BrandImages/', width_field='width_field')),
                ('height_field', models.IntegerField(default=0)),
                ('width_field', models.IntegerField(default=0)),
                ('deleteImg', models.BooleanField(default=False)),
                ('proCatId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proCatImages', to='Categories.ProductCategories')),
            ],
        ),
        migrations.AddField(
            model_name='brandimages',
            name='brandId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brandImages', to='Categories.Brands'),
        ),
    ]