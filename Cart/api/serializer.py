from rest_framework import serializers
from Cart.models import Cart,CartProducts
from Products.models import Products,ProductCombinations,ProductCombinationImages,VariantValues,Variants,CombinationValues,ProductVendor,Offer,OfferProductVendors
import datetime
from django.utils import timezone
from User.models import PromoCodes,UsedPromoCodes
from django.conf import settings

class AddToCartValidateSerializer (serializers.ModelSerializer):

    qty = serializers.IntegerField()
    productId = serializers.IntegerField()
    hasVariants = serializers.BooleanField()
    if hasVariants == 'true':
        proVarId = serializers.IntegerField()


    class Meta:
        model = CartProducts
        fields = ('productId','proVarId','qty','hasVariants')

class UpdateCartProSerializer (serializers.ModelSerializer):

    cartProductId = serializers.IntegerField()
    qty = serializers.IntegerField()

    class Meta:
        model = CartProducts
        fields = ('cartProductId','qty',  )


class OfferSerializer (serializers.ModelSerializer):

    is_valid = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = '__all__'

    def get_is_valid (self,obj):

        try:
            off = Offer.objects.get(offerId=obj.offerId,endDate__gte = datetime.datetime.now(),startDate__lte = datetime.datetime.now(),isLive=True,deleteOffer = False)
            return True
        except:
            return False
        

class OfferProductVendorSerializer (serializers.ModelSerializer):

    #offerId = OfferSerializer(many=False)
   # is_valid = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    class Meta:
        model = OfferProductVendors
        fields = '__all__'

    def get_is_valid (self,obj):
        try:
            off = Offer.objects.get(offerId=obj.offerId.offerId,endDate__gte = datetime.datetime.now(),startDate__lte = datetime.datetime.now(),isLive=True,deleteOffer = False)
            return True
        except:
            return False

    def get_title (self,obj):

        try:
            off = Offer.objects.get(offerId=obj.offerId.offerId)
            return off.offerTitle
        except:
            return None

        

class VariantSerializer (serializers.ModelSerializer):

    class Meta:
        model = Variants
        fields = ('variantTitle',)


class ProductImageSerializer (serializers.ModelSerializer):

    class Meta:
        model = ProductCombinationImages
        fields = ('proVarImg','deleteImg')

class ProductSerializer (serializers.ModelSerializer):

    Images = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='productcombinationimages-detail'
    )

    price = serializers.SerializerMethodField()


    class Meta:
        model = Products
        fields = '__all__'

    def get_price (self,product):

        request = self.context['request']
        if not product.hasVariants:
            price = ProductVendor.objects.filter(product=product,vendorId=int(request.query_params['vendorId']))
            ser = ProductVendorSerializer(instance=price,many=True)
            return ser.data

        return []


class VariantValuesSerializer (serializers.ModelSerializer):

    varId = VariantSerializer()

    class Meta:
        model = VariantValues
        fields = ('varValue','varId')

class ProductVendorSerializer(serializers.ModelSerializer):

    Offers = serializers.SerializerMethodField()

    class Meta:
        model = ProductVendor
        fields = '__all__'

    def get_Offers(self,obj):

        offer = OfferProductVendors.objects.filter(proVendorId = obj,isLive=True,deleteOfferPro=False)
        ser = OfferProductVendorSerializer(instance = offer,many = True )
        return ser.data      
        


class CombinationValuesSerializer (serializers.ModelSerializer):

   # variantValue = VariantValuesSerializer(many=False)
    variant = serializers.SerializerMethodField()
    value =serializers.SerializerMethodField()

    class Meta:
        model = CombinationValues
        fields = ('variant','value',)

    def get_variant(self,cv):
        return cv.variantValue.varId.variantTitle
    
    def get_value (self,cv):
        return cv.variantValue.varValue

class ProductCombinationSerializer (serializers.ModelSerializer):

    combValues = CombinationValuesSerializer(many=True)
    #price = serializers.SerializerMethodField()
    Images = ProductImageSerializer(many=True)

    class Meta:
        model = ProductCombinations
        fields = '__all__'

    #ef get_price (self,product):

    #   request = self.context['request']
    #   price = ProductVendor.objects.filter(proVarId=product,vendorId=int(request.query_params['vendorId']))
    #   ser = ProductVendorSerializer(instance=price,many=True)
    #   return ser.data

class GetCartProductsSerializer (serializers.ModelSerializer):

    #product = ProductSerializer(many=False)
    #proVarId = ProductCombinationSerializer(many=False)
    price = serializers.SerializerMethodField()
    selectedVariants = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    hasVariants = serializers.SerializerMethodField()
    Image = serializers.SerializerMethodField()
    isStock = serializers.SerializerMethodField()
    Offer = serializers.SerializerMethodField()
    proVendorId = serializers.SerializerMethodField()
    

    class Meta :
        model = CartProducts
        fields = '__all__'

    def get_Offer (self,cp):

        proVendor = {}
        request = self.context['request']
       # return request.query_params['vendorId']
        if cp.proVarId:
            proVendor = ProductVendor.objects.get(vendorId=int(request.query_params['vendorId']),proVarId = cp.proVarId)
        else:    
            proVendor = ProductVendor.objects.get(vendorId=int(request.query_params['vendorId']),product = cp.product)

        #return proVendor.pk
        try:
            offer = OfferProductVendors.objects.get(proVendorId=proVendor,isLive=True,deleteOfferPro = False)
            if offer.offerId.is_valid:
                return offer.offerPrice
        except:
            return
         

    def get_id (self,cp):

        return cp.product.pk

    def get_title (self,cp):

        return cp.product.productTitle

    def get_hasVariants (self,cp):

        return cp.product.hasVariants

    def get_isStock (self,cp):

        request = self.context['request']
        #return request.query_params['vendorId']
        if cp.proVarId:
            proVendor = ProductVendor.objects.get(vendorId__pk=int(request.query_params['vendorId']),proVarId = cp.proVarId)
            return proVendor.isStock
        proVendor = ProductVendor.objects.get(vendorId__pk=int(request.query_params['vendorId']),product = cp.product)
        return proVendor.isStock

    def get_proVendorId (self,cp):

        request = self.context['request']
        #return request.query_params['vendorId']
        if cp.proVarId:
            proVendor = ProductVendor.objects.get(vendorId=int(request.query_params['vendorId']),proVarId = cp.proVarId.pk)
            return proVendor.pk
        proVendor = ProductVendor.objects.get(vendorId=int(request.query_params['vendorId']),product = cp.product.pk)
        return proVendor.pk


    def get_Image (self,cp):

        if cp.proVarId:
            image = ProductCombinationImages.objects.filter(proVarId = cp.proVarId,deleteImg=False)
            if len(image) is not 0 :
                return getattr(settings,'CUSTOM_DOMAIN','http://localhost:8000/media/')+str(image[0].proVarImg)
            return ""    
        image = ProductCombinationImages.objects.filter(product = cp.product,deleteImg=False)
        if len(image) is not 0 :
            return getattr(settings,'CUSTOM_DOMAIN','http://localhost:8000/media/')+str(image[0].proVarImg)
        return ""


    def get_price (self,cp):

        request = self.context['request']
        #return request.query_params['vendorId']
        if cp.proVarId:
            proVendor = ProductVendor.objects.get(vendorId=int(request.query_params['vendorId']),proVarId = cp.proVarId)
            return proVendor.sellPrice
        proVendor = ProductVendor.objects.get(vendorId=int(request.query_params['vendorId']),product = cp.product)
        return proVendor.sellPrice
    
    def get_selectedVariants (self,cp):

        if cp.product.hasVariants:
            combVal = CombinationValues.objects.filter(proCombId = cp.proVarId,isLive=True,delete = False)
            ser = CombinationValuesSerializer(instance=combVal,many=True)
            return ser.data
        return []


class GetCartSerializer (serializers.ModelSerializer):

    CartProducts = GetCartProductsSerializer(many=True)
    totalPrice = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('__all__')

    def get_totalPrice (self,obj):

        request = self.context['request']

        cp = CartProducts.objects.filter(cartId = obj,deleteCartProduct = False)
        total = 0
        for cartPro in cp:

            if cartPro.product.hasVariants:
                try:
                    proVendor = ProductVendor.objects.get(vendorId=int(request.query_params['vendorId']),proVarId = cartPro.proVarId,isStock = True,deleteProVendor = False,isLive = True)
                    
                    try:
                        offer = OfferProductVendors.objects.get(proVendorId=proVendor,isLive=True,deleteOfferPro = False)
                        if offer.offerId.is_valid:
                            total += (offer.offerPrice*cartPro.qty)

                        else:
                            total += (offer.sellPrice*cartPro.qty)
                    except:
                        total += (proVendor.sellPrice*cartPro.qty)
                except:
                    pass

            else:
                try:
                    proVendor = ProductVendor.objects.get(vendorId=int(request.query_params['vendorId']),product = cartPro.product,isStock = True,deleteProVendor = False,isLive = True)
                
                    try:
                        offer = OfferProductVendors.objects.get(proVendorId=proVendor,isLive=True,deleteOfferPro = False)
                        if offer.offerId.is_valid:
                            total += (offer.offerPrice*cartPro.qty)
                        else:
                            total += (proVendor.sellPrice*cartPro.qty)

                    except:
                        total += (proVendor.sellPrice*cartPro.qty)        
                except:
                    pass
        return total

    def get_count(self,obj):

        request = self.context['request']

        cp = CartProducts.objects.filter(cartId = obj,deleteCartProduct = False)
        count = 0
        for cartPro in cp:

            if cartPro.product.hasVariants:
                try:
                    proVendor = ProductVendor.objects.get(vendorId=int(request.query_params['vendorId']),proVarId = cartPro.proVarId,isStock = True,deleteProVendor = False,isLive = True)
                
                    count += cartPro.qty
                except:
                    pass
            else:
                try:
                    proVendor = ProductVendor.objects.get(vendorId=int(request.query_params['vendorId']),product = cartPro.product,isStock = True,deleteProVendor = False,isLive = True)
                
                    count += cartPro.qty
                except:
                    pass
        return count


class PromoCodeSerializer (serializers.ModelSerializer):

    class Meta:
        model = PromoCodes,
        fields = '__all__'



class GetCartProductsSerializerForOrder (serializers.ModelSerializer):

    
    price = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    
    

    class Meta :
        model = CartProducts
        fields = ('id','price','title','qty',)

    
         

    def get_id (self,cp):

        return cp.product.pk

    def get_title (self,cp):

        return cp.product.productTitle

    def get_hasVariants (self,cp):

        return cp.product.hasVariants

    

 
    def get_price (self,cp):

        request = self.context['request']
        proVendor = {}
        if cp.proVarId:
            proVendor = ProductVendor.objects.get(vendorId=int(request.query_params['vendorId']),proVarId = cp.proVarId.pk)
            
        else:    
            proVendor = ProductVendor.objects.get(vendorId=int(request.query_params['vendorId']),product = cp.product.pk)
        

        try:
            offer = OfferProductVendors.objects.get(proVendorId=proVendor,isLive=True,deleteOfferPro = False)
            if offer.offerId.is_valid:
                return {
                    "sellPrice":proVendor.sellPrice,
                    "costPrice":proVendor.costPrice,
                    "isStock" : proVendor.isStock,
                    "offerPrice" : offer.offerPrice,
                    "offerId" : offer.offerId.pk,
                    "proVendorId":proVendor.pk
                }
            return {
                    "sellPrice":proVendor.sellPrice,
                    "costPrice":proVendor.costPrice,
                    "isStock" : proVendor.isStock,
                    "offerPrice" : None,
                    "offerId" : None,
                    "proVendorId":proVendor.pk
                }
            
        except:
            return {
                    "sellPrice":proVendor.sellPrice,
                    "costPrice":proVendor.costPrice,
                    "isStock" : proVendor.isStock,
                    "offerPrice" : None,
                    "offerId" : None,
                    "proVendorId":proVendor.pk
                }
    
    


class GetCartSerializerForOrder (serializers.ModelSerializer):

    CartProducts = GetCartProductsSerializerForOrder(many=True)
    totalPrice = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('CartProducts','totalPrice','count',)

    def get_totalPrice (self,obj):

        request = self.context['request']

        cp = CartProducts.objects.filter(cartId = obj,deleteCartProduct = False)
        total = 0
        for cartPro in cp:

            if cartPro.product.hasVariants:
                try:
                    proVendor = ProductVendor.objects.get(vendorId=int(request.query_params['vendorId']),proVarId = cartPro.proVarId,isStock = True,deleteProVendor = False,isLive = True)
                    
                    try:
                        offer = OfferProductVendors.objects.get(proVendorId=proVendor,isLive=True,deleteOfferPro = False)
                        if offer.offerId.is_valid:
                            total += (offer.offerPrice*cartPro.qty)
                    except:
                        total += (proVendor.sellPrice*cartPro.qty)
                except:
                    pass

            else:
                try:
                    proVendor = ProductVendor.objects.get(vendorId=int(request.query_params['vendorId']),product = cartPro.product,isStock = True,deleteProVendor = False,isLive = True)
                
                    try:
                        offer = OfferProductVendors.objects.get(proVendorId=proVendor,isLive=True,deleteOfferPro = False)
                        if offer.offerId.is_valid:
                            total += (offer.offerPrice*cartPro.qty)
                    except:
                        total += (proVendor.sellPrice*cartPro.qty)        
                except:
                    pass
        return total

    def get_count(self,obj):

        request = self.context['request']

        cp = CartProducts.objects.filter(cartId = obj,deleteCartProduct = False)
        count = 0
        for cartPro in cp:

            if cartPro.product.hasVariants:
                try:
                    proVendor = ProductVendor.objects.get(vendorId=int(request.query_params['vendorId']),proVarId = cartPro.proVarId,isStock = True,deleteProVendor = False,isLive = True)
                
                    count += cartPro.qty
                except:
                    pass
            else:
                try:
                    proVendor = ProductVendor.objects.get(vendorId=int(request.query_params['vendorId']),product = cartPro.product,isStock = True,deleteProVendor = False,isLive = True)
                
                    count += cartPro.qty
                except:
                    pass
        return count
