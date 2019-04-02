from django.db import models
from User.models import User
from Products.models import ProductCombinations,Products

# Create your models here.
class Cart (models.Model):

    cartId = models.AutoField(primary_key = True)
    customerId = models.ForeignKey(User,on_delete=models.CASCADE,related_name="Cart")
    deleteCart = models.BooleanField(default=False)

class CartProducts(models.Model):

    cartProductId = models.AutoField(primary_key = True)
    cartId = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="CartProducts")
    proVarId = models.ForeignKey(ProductCombinations,on_delete=models.CASCADE,related_name="CurrentInCart",blank=True,null=True)
    product = models.ForeignKey(Products,on_delete=models.CASCADE,related_name="CurrentInCart")
    qty = models.PositiveIntegerField()
    deleteCartProduct = models.BooleanField(default=False)
    
