from rest_framework import serializers
from User.models import Area,User,Verification,UserAddress
from phonenumber_field.formfields import PhoneNumberField
from Orders.models import Orders,OrderProducts
from Cart.api.serializer import CombinationValuesSerializer
from Products.models import ProductCombinationImages
from django.conf import settings
from Products.models import CombinationValues


class VendorSerializer (serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','name','is_vendor')

class AreaSerializer (serializers.ModelSerializer):

    Users = VendorSerializer(many=True)

    class Meta:
        model = Area
        fields = '__all__'

class CreateOTPSerializer(serializers.ModelSerializer):

    phone = serializers.CharField(validators=PhoneNumberField().validators)
    #pk = serializers.IntegerField()
    class Meta:
        model = Verification
        fields = ('pk','phone')

class ValidateOTPSerializer (serializers.ModelSerializer):

    pk = serializers.IntegerField()
    otp = serializers.CharField(max_length=40)

    class Meta:
        model = Verification
        fields = ('pk','otp')



class UpdateNameSerializer (serializers.Serializer):

    name = serializers.CharField(max_length = 20)

class UserAddressSerializer (serializers.ModelSerializer):

    class Meta:
        model = UserAddress
        fields = ('pk','address',)

class MyProfileSerializer (serializers.ModelSerializer):

    Address = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('name','Address','dateOfJoin','phone')

    def get_Address (self,user):

        try:
            ua = UserAddress.objects.filter(deleteAddress = False,userId=user)
            ser = UserAddressSerializer(instance = ua ,many = True)
            return ser.data

        except:
            return []

class OrderProductsSerializer (serializers.ModelSerializer):

    title = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    selectedVariants = serializers.SerializerMethodField()
    hasVariants = serializers.SerializerMethodField()

    class Meta:
        model = OrderProducts
        fields = ('title','image','price','discount','selectedVariants','hasVariants','qty')
    
    def get_title (self,op):
        return op.proVendorId.product.productTitle

    def get_image (self,op):
        if op.proVendorId.product.hasVariants :
            image = ProductCombinationImages.objects.filter(proVarId = op.proVendorId.proVarId,deleteImg = False).first()
            return getattr(settings,'CUSTOM_DOMAIN','http://localhost:8000/media/')+str(image.proVarImg)

        image = ProductCombinationImages.objects.filter(product = op.proVendorId.product,deleteImg = False).first()
        return getattr(settings,'CUSTOM_DOMAIN','http://localhost:8000/media/')+str(image.proVarImg)

    def get_price (self,op):

        return op.sellPrice

    def get_discount (self,op):

        return op.discountPrice

    def get_selectedVariants (self,op):

        if op.proVendorId.product.hasVariants :
            combVal = CombinationValues.objects.filter(proCombId = op.proVendorId.proVarId,isLive=True,delete = False)
            ser = CombinationValuesSerializer(instance = combVal , many=True)
            return ser.data
        return []

    def get_hasVariants (self,op):

        return op.proVendorId.product.hasVariants



        


class MyOrdersSerializer (serializers.ModelSerializer):

    totalAmount = serializers.DecimalField(source='get_totalSellPrice',max_digits=10,decimal_places = 2)
    orderStatus = serializers.SerializerMethodField()
    orderProducts = serializers.SerializerMethodField() 

    class Meta :
        model = Orders
        fields = ('totalAmount','orderStatus','deliverAddress','promoCodeId','discountPrice','invoiceNo','orderProducts','orderDate',)

    def get_orderStatus (self,order):

        if order.orderStatus is 0:
            return "Proccessing"

        if order.orderStatus is 1 :
            return "Dispatched"

        if order.orderStatus is 2 :
            return "Delivered"

        if order.orderStatus is 3 :
            return "Cancelled"

    def get_orderProducts (self,order):

        op = OrderProducts.objects.filter(orderId = order,deleteOrderProduct = False)
        ser = OrderProductsSerializer(instance = op ,many=True)
        return ser.data

class EditAddress (serializers.Serializer):

    id = serializers.IntegerField()
    address = serializers.CharField(max_length = 60)

class DeleteAddress (serializers.Serializer):

    id = serializers.IntegerField()

class AddAddress (serializers.Serializer):

    address = serializers.CharField(max_length = 60)
    

