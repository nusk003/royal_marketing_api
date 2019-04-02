from django.db import models
from Orders.models import Orders
# Create your models here.

class Payment (models.Model):

    paymentId = models.AutoField(primary_key = True)
    orderId = models.ForeignKey(Orders,on_delete=models.CASCADE,related_name="Payment")
    paymentDate = models.DateTimeField(auto_now=True)

    
    