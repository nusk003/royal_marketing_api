# Generated by Django 2.1.3 on 2018-12-20 11:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import optimized_image.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaints',
            fields=[
                ('complaintId', models.AutoField(primary_key=True, serialize=False)),
                ('complaintBody', models.CharField(max_length=500)),
                ('complaintStatus', models.IntegerField()),
                ('complaintDate', models.DateTimeField(auto_now=True)),
                ('deleteComplaint', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ComplaintType',
            fields=[
                ('complaintTypeId', models.AutoField(primary_key=True, serialize=False)),
                ('complaintType', models.CharField(max_length=20)),
                ('deleteType', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('deleveryId', models.AutoField(primary_key=True, serialize=False)),
                ('dispatchedDate', models.DateTimeField()),
                ('deliveredDate', models.DateTimeField()),
                ('note', models.CharField(max_length=500)),
                ('deleteDelivery', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ExpressCheckout',
            fields=[
                ('expressCheckoutId', models.AutoField(primary_key=True, serialize=False)),
                ('image', optimized_image.fields.OptimizedImageField(upload_to='ExpressCheckouts/')),
                ('invoiceNo', models.CharField(max_length=20)),
                ('orderStatus', models.IntegerField()),
                ('deleteExpress', models.BooleanField(default=False)),
                ('customerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ExpressCheckouts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderProducts',
            fields=[
                ('orderProductId', models.AutoField(primary_key=True, serialize=False)),
                ('qty', models.PositiveIntegerField()),
                ('costPrice', models.DecimalField(decimal_places=2, max_digits=7)),
                ('sellPrice', models.DecimalField(decimal_places=2, max_digits=7)),
                ('isCancel', models.BooleanField(default=False)),
                ('discountPrice', models.DecimalField(decimal_places=2, max_digits=7)),
                ('deleteOrderProduct', models.BooleanField(default=False)),
                ('cancelReason', models.CharField(blank=True, max_length=100, null=True)),
                ('offerProductVendorsId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='OrderProducts', to='Products.OfferProductVendors')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('orderId', models.AutoField(primary_key=True, serialize=False)),
                ('invoiceNo', models.CharField(max_length=12)),
                ('isExpressCheckout', models.BooleanField(default=False)),
                ('orderDate', models.DateTimeField(auto_now=True)),
                ('orderStatus', models.IntegerField()),
                ('deliverAddress', models.CharField(default='Main Road', max_length=50)),
                ('dueSellPrice', models.DecimalField(decimal_places=2, default=200.0, max_digits=10)),
                ('dueCostPrice', models.DecimalField(decimal_places=2, default=200.0, max_digits=10)),
                ('discountPrice', models.DecimalField(decimal_places=2, default=200.0, max_digits=10)),
                ('deleteOrder', models.BooleanField(default=False)),
                ('cancelReason', models.CharField(blank=True, max_length=100, null=True)),
                ('customerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Orders', to=settings.AUTH_USER_MODEL)),
                ('expressCheckoutId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Orders.ExpressCheckout')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('paymentTypeId', models.AutoField(primary_key=True, serialize=False)),
                ('paymentType', models.CharField(max_length=20)),
                ('deletePaymentType', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('requestId', models.AutoField(primary_key=True, serialize=False)),
                ('requestBody', models.CharField(max_length=500)),
                ('requestStatus', models.IntegerField()),
                ('requestDate', models.DateTimeField(auto_now=True)),
                ('deleteRequest', models.BooleanField(default=False)),
                ('customerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RequestType',
            fields=[
                ('requestTypeID', models.AutoField(primary_key=True, serialize=False)),
                ('requestType', models.CharField(max_length=20)),
                ('deleteRequestType', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ReturnProducts',
            fields=[
                ('returnId', models.AutoField(primary_key=True, serialize=False)),
                ('qty', models.PositiveIntegerField()),
                ('reason', models.CharField(max_length=500)),
                ('deleteReturn', models.BooleanField(default=False)),
                ('orderId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ReturnProducts', to='Orders.Orders')),
                ('productVendorId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Returns', to='Products.ProductVendor')),
            ],
        ),
        migrations.AddField(
            model_name='requests',
            name='requestType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Requests', to='Orders.RequestType'),
        ),
        migrations.AddField(
            model_name='orders',
            name='paymentType',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Orders', to='Orders.PaymentType'),
        ),
        migrations.AddField(
            model_name='orders',
            name='promoCodeId',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Orders', to='User.PromoCodes'),
        ),
        migrations.AddField(
            model_name='orderproducts',
            name='orderId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='OrderProducts', to='Orders.Orders'),
        ),
        migrations.AddField(
            model_name='orderproducts',
            name='proVendorId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ProductVendors', to='Products.ProductVendor'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='orderId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Delivery', to='Orders.Orders'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='riderId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Deliveries', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='complaints',
            name='complaintType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Complaints', to='Orders.ComplaintType'),
        ),
        migrations.AddField(
            model_name='complaints',
            name='customerId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Complaints', to=settings.AUTH_USER_MODEL),
        ),
    ]
