from django.db import models
from django.db.models import Sum,Count,Avg,F

from User.models import (User,PromoCodes)
from Products.models import (
    ProductCombinations,
ProductVendor,OfferProductVendors)
from optimized_image.fields import OptimizedImageField

# Create your models here.
class PaymentType (models.Model):

    paymentTypeId = models.AutoField(primary_key = True)
    paymentType = models.CharField(max_length = 20)
    deletePaymentType = models.BooleanField(default=False)

class ExpressCheckout (models.Model):

    expressCheckoutId = models.AutoField(primary_key = True)
    customerId = models.ForeignKey(User,on_delete=models.CASCADE,related_name="ExpressCheckouts")
    image = OptimizedImageField(upload_to = "ExpressCheckouts/")
    invoiceNo = models.CharField(max_length = 20)
    orderStatus = models.IntegerField()
    deleteExpress = models.BooleanField(default=False)

class Orders (models.Model):

    orderId = models.AutoField(primary_key = True)
    customerId = models.ForeignKey(User,on_delete=models.CASCADE,related_name="Orders")
    invoiceNo = models.CharField(max_length = 12)
    isExpressCheckout = models.BooleanField(default=False)
    expressCheckoutId = models.ForeignKey(ExpressCheckout,on_delete=models.CASCADE,blank = True ,null = True)
    orderDate = models.DateTimeField(auto_now=True)
    orderStatus = models.IntegerField()
    deliverAddress = models.CharField(max_length = 50,default="Main Road")
    promoCodeId = models.ForeignKey(PromoCodes,on_delete=models.CASCADE,related_name="Orders",blank=True,null = True)
    #dueSellPrice = models.DecimalField(max_digits=10,decimal_places=2,default = 200.00)
    #dueCostPrice = models.DecimalField(max_digits=10,decimal_places=2,default = 200.00)
    discountPrice = models.DecimalField(max_digits=10,decimal_places=2,default = 200.00)
    paymentType = models.ForeignKey(PaymentType,on_delete=models.CASCADE,related_name="Orders",default=1)    
    deleteOrder = models.BooleanField(default=False)
    cancelReason = models.CharField(max_length = 100,blank = True ,null = True)

    
    def get_totalSellPrice (self) :
        
        try:
            ops = OrderProducts.objects.filter(orderId = self,deleteOrderProduct = False,isCancel =False)
            totalPrice = 0
            for op in ops:
                if op.discountPrice is not None:
                    totalPrice += (op.discountPrice*op.qty)
                else:
                    totalPrice += (op.sellPrice*op.qty)

            return totalPrice
        except:
            return 0  
    def get_totalCostPrice (self) :

        total = OrderProducts.objects.filter(orderId = self,deleteOrderProduct = False,isCancel =False).annotate(totalPrice = Sum(F('costPrice') * F('qty'),output_field=models.DecimalField(max_digits=10,decimal_places=2)))
        return total.first().totalPrice

class OrderProducts(models.Model):

    orderProductId = models.AutoField(primary_key=True)
    orderId = models.ForeignKey(Orders,on_delete=models.CASCADE,related_name="OrderProducts")
    proVendorId = models.ForeignKey(ProductVendor,on_delete=models.CASCADE,related_name="ProductVendors")
    qty = models.PositiveIntegerField()
    costPrice = models.DecimalField(max_digits=7,decimal_places=2)
    sellPrice = models.DecimalField(max_digits=7,decimal_places=2)
    isCancel = models.BooleanField(default=False)
    discountPrice = models.DecimalField(max_digits=7, decimal_places=2, blank = True,null = True)
    offerProductVendorId = models.ForeignKey(OfferProductVendors,on_delete=models.CASCADE,related_name="OrderProducts",blank=True,null=True)
    deleteOrderProduct = models.BooleanField(default=False)
    cancelReason = models.CharField(max_length = 100,blank = True ,null = True)

class Delivery(models.Model):

    deleveryId = models.AutoField(primary_key = True)
    orderId = models.ForeignKey(Orders,on_delete=models.CASCADE,related_name="Delivery")
    riderId = models.ForeignKey(User,on_delete=models.CASCADE,related_name="Deliveries")
    dispatchedDate = models.DateTimeField()
    deliveredDate = models.DateTimeField()
    note = models.CharField(max_length = 500)
    deleteDelivery = models.BooleanField(default=False)

class ReturnProducts(models.Model):

    returnId = models.AutoField(primary_key = True)
    orderId = models.ForeignKey(Orders,on_delete=models.CASCADE,related_name="ReturnProducts")
    productVendorId = models.ForeignKey(ProductVendor,on_delete=models.CASCADE,related_name="Returns")
    qty = models.PositiveIntegerField()
    reason = models.CharField(max_length=500)
    deleteReturn = models.BooleanField(default=False)

class ComplaintType (models.Model):

    complaintTypeId = models.AutoField(primary_key = True)
    complaintType = models.CharField(max_length = 20)
    deleteType = models.BooleanField(default=False)

class Complaints (models.Model):

    complaintId = models.AutoField(primary_key = True)
    customerId = models.ForeignKey(User,on_delete=models.CASCADE,related_name="Complaints")
    complaintType = models.ForeignKey(ComplaintType,on_delete=models.CASCADE,related_name="Complaints")
    complaintBody = models.CharField(max_length = 500)
    complaintStatus = models.IntegerField()
    complaintDate = models.DateTimeField(auto_now=True)
    deleteComplaint = models.BooleanField(default=False)

class RequestType (models.Model):

    requestTypeID = models.AutoField(primary_key = True)
    requestType  = models.CharField(max_length = 20)
    deleteRequestType = models.BooleanField(default=False)

class Requests (models.Model):

    requestId = models.AutoField(primary_key = True)
    customerId = models.ForeignKey(User,on_delete = models.CASCADE,related_name="Requests")
    requestType = models.ForeignKey(RequestType,on_delete=models.CASCADE,related_name="Requests")
    requestBody = models.CharField(max_length = 500)
    requestStatus = models.IntegerField()
    requestDate = models.DateTimeField(auto_now=True)
    deleteRequest = models.BooleanField(default=False)



