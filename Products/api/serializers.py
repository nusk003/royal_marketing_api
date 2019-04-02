from rest_framework import serializers
from Products.models import (Variants,
                            VariantValues,
                            Products,
                            ProductCategories,
                            Categories,
                            Brands,
                            CombinationValues,
                            ProductCombinations,
                            ProductCombinationImages,
                            ProductCombinationKeywords,
                            ProductVendor,
                            Offer,
                            OfferProductVendors,
                            Review,
                            User
                            )
from rest_framework.response import Response
from User.models import User
from django.db.models import Min
from Cart.api.serializer import CombinationValuesSerializer as cvs
import datetime
from collections import OrderedDict
from django.db.models import Min
from django.conf import settings

class VariantTypeSerializer (serializers.ModelSerializer):

    class Meta:
        model = Variants
        fields = '__all__'

class VariantValuesSerializer (serializers.ModelSerializer):

    varId = VariantTypeSerializer()
    
    class Meta:
        model = VariantValues
        fields = '__all__'

class ProductCombinationImagesSerializer (serializers.ModelSerializer):

    class Meta:
        model = ProductCombinationImages
        fields = '__all__'
        read_only_fields = ('proVarId','product')

    def create(self,validated_data):

        pc = ProductCombinations.objects.get(pk=1)
        image = ProductCombinationImages.objects.create(**validated_data,proVarId=pc)
        return image

class ProductCombinationsKeywordsSerializer (serializers.ModelSerializer):

    class Meta:
        model = ProductCombinationKeywords
        fields = '__all__'
        read_only_fields = ('proVarId','product')

class CombinationValuesSerializer (serializers.ModelSerializer):
    
    class Meta:
        model = CombinationValues
        fields = '__all__'
        read_only_fields = ('proCombId','product')


class ProductVendorSerializer (serializers.ModelSerializer):

    class Meta:
        model = ProductVendor
        fields = '__all__'
        read_only_fields = ('proVarId','product')

class ProductCombinationSerializer (serializers.ModelSerializer):

    prices  = ProductVendorSerializer(many=True)
    Keywords = ProductCombinationsKeywordsSerializer(many=True)
    Images = ProductCombinationImagesSerializer(many=True)
    combValues = CombinationValuesSerializer(many=True)

    class Meta:
        model = ProductCombinations
        fields = '__all__'
        read_only_fields = ('product',)

class ProductSerializer (serializers.ModelSerializer):

    Combinations = ProductCombinationSerializer(many=True)
    Images = ProductCombinationImagesSerializer(many=True)
    prices = ProductVendorSerializer(many=True)
    Keywords = ProductCombinationsKeywordsSerializer(many=True)

    class Meta:
        model = Products
        fields = '__all__'

    def create (self,validated_data):
        
        Combinations = validated_data.pop('Combinations')
        proPrices = validated_data.pop('prices')
        proImages = validated_data.pop('Images')
        proKeywords = validated_data.pop('Keywords')
       
        product = Products.objects.create(**validated_data)
         
        if product.hasVariants:
            
            for combination in Combinations:
                prices = combination.pop('prices')
                Keywords = combination.pop('Keywords')
                Images = combination.pop('Images')
                combValues = combination.pop('combValues')
                productComb = ProductCombinations.objects.create(**combination,product=product)
                for combValue in combValues:
                    CombinationValues.objects.create(**combValue,proCombId=productComb)
                for vendor in prices:
                    ProductVendor.objects.create(**vendor,proVarId = productComb,product=product)
                for keyword in Keywords:
                    ProductCombinationKeywords.objects.create(**keyword,proVarId=productComb,product=product)
                for image in Images:
                    ProductCombinationImages.objects.create(**image,proVarId = productComb,product=product)

        else:
            for proImage in proImages:
                ProductCombinationImages.objects.create(**proImage,proVarId=None,product=product)
            for vendor in proPrices:
                ProductVendor.objects.create(**vendor,proVarId = None,product=product)
            for keyword in proKeywords:
                ProductCombinationKeywords.objects.create(**keyword,proVarId=None,product=product)

        return product

class CreateVariantValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = VariantValues
        fields = ('__all__')

class OfferProductVendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfferProductVendors
        fields = '__all__'        

class FeatureProductVendorSerializer (serializers.ModelSerializer):

    Offers = OfferProductVendorSerializer(many=True)

    class Meta:
        model = ProductVendor
        fields = ('proVendorId','sellPrice','isStock','Offers','proVarId')

class FeatureProductImageSerializer (serializers.ModelSerializer):

    class Meta:
        model = ProductCombinationImages
        fields = ('proVarImg','deleteImg',)

class FeatureProductSerializer(serializers.ModelSerializer):

    price = serializers.SerializerMethodField()
    Image = serializers.SerializerMethodField()
    isStock = serializers.SerializerMethodField()
    combination = serializers.SerializerMethodField()
    Offer = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = ('__all__')

    def get_Offer (self,product):

        request = self.context['request']
        try:
            proVendor = ProductVendor.objects.filter(product=product,vendorId=int(request.query_params['vendorId']),deleteProVendor=False,isLive=True).order_by('sellPrice')[:1]
            offer = OfferProductVendors.objects.get(isLive=True,deleteOfferPro = False,proVendorId = proVendor)
            if offer.offerId.is_valid :
                return offer.offerPrice
            

        except:
            pass 

    def get_combination (self,product):

        request = self.context['request']
        try:
            proVendor = ProductVendor.objects.filter(product=product,vendorId=int(request.query_params['vendorId']),deleteProVendor=False,isLive=True).order_by('sellPrice')[:1]
            combVal = CombinationValues.objects.filter(proCombId = proVendor[0].proVarId,isLive=True,delete = False)
            ser = cvs(instance=combVal,many=True)
            return ({
                "id":proVendor[0].proVarId.pk,
                "variants":ser.data
            })

        except:
            pass 


    def get_isStock(self,product):

        request = self.context['request']
        try:
            proVendor = ProductVendor.objects.filter(product=product,vendorId=int(request.query_params['vendorId']),deleteProVendor=False,isLive=True).order_by('sellPrice')[:1]
            return proVendor[0].isStock
        except:
            pass 

    def get_price (self,product):

        request = self.context['request']
        try:
            proVendor = ProductVendor.objects.filter(product=product,vendorId=int(request.query_params['vendorId']),deleteProVendor=False,isLive=True).order_by('sellPrice')[:1]
            return proVendor[0].sellPrice
        except:
            pass   
    
        

    def get_Image (self,product):

        image = ProductCombinationImages.objects.filter(product=product,deleteImg=False).order_by('pk')[:1]
        
        return getattr(settings,'CUSTOM_DOMAIN','http://localhost:8000/media/')+str(image[0].proVarImg)

class ProductCombinationDetSerializer(serializers.ModelSerializer):

    price = serializers.SerializerMethodField()
   # offer = serializers.SerializerMethodField()
    values = serializers.SerializerMethodField()
    Images = serializers.SerializerMethodField()

    class Meta:
        model = ProductCombinations
        fields = ('price','values','pk','Images',)

    def get_price(self,pc):
        
        #request = self.context['request']
        #vendor = User.objects.get(pk = request.query_params['vendorId'])
        #return request.query_params['vendorId']
        try:
            proVendor = ProductVendor.objects.get(vendorId = 1,isLive = True ,deleteProVendor = False,proVarId = pc)
            
            try:
                offerPro = OfferProductVendors.objects.get(
                        proVendorId = proVendor,
                        deleteOfferPro = False , 
                        isLive = True ,
                        offerId__deleteOffer = False,
                        offerId__isLive = True,
                        offerId__startDate__lte = datetime.datetime.now(),
                        offerId__endDate__gte = datetime.datetime.now()
                        )
                
                return {
                "sellPrice":proVendor.sellPrice,
                "isStock" : proVendor.isStock,
                "offerPrice" : offerPro.offerPrice 
                }
                

            except:
                return {
                    "sellPrice":proVendor.sellPrice,
                    "isStock" : proVendor.isStock,
                    "offerPrice" : None
                }
                

        except:
            pass

    def get_values(self,pc):

        combValues = CombinationValues.objects.filter(proCombId = pc,isLive = True,delete = False)
        values = []
        for combValue in combValues:
            values.append(combValue.variantValue.varValue)
        return values

    def get_Images (self,pc):

        images = ProductCombinationImages.objects.filter(proVarId = pc,deleteImg = False)
        img_list = []
        for image in images:
            img_list.append(getattr(settings,'CUSTOM_DOMAIN','http://localhost:8000/media/')+str(image.proVarImg))

        return img_list



class ProductDetailsSerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    Images = serializers.SerializerMethodField()
    variants = serializers.SerializerMethodField()
    hasVariants = serializers.SerializerMethodField()
    combinations = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    #isStock = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    productCat = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    defaultComb = serializers.SerializerMethodField()
    #offer = serializers.SerializerMethodField()
    related = serializers.SerializerMethodField()
    class Meta:
        model = Products
        fields = ('id','title','Images','variants','hasVariants','combinations','reviews','description','category','productCat','brand','price','defaultComb','related',)

    def get_id (self,product):

        return product.pk

    def get_title (self,product):

       return product.productTitle

    def get_Images (self,product):

        try:
            images = ProductCombinationImages.objects.filter(product = product,deleteImg=False)
            image_urls = []
            for image in images:
                image_urls.append(getattr(settings,'CUSTOM_DOMAIN','http://localhost:8000/media/')+str(image.proVarImg))

            return image_urls
        except:
            return []

    def get_defaultComb (self,product):

        if product.hasVariants:
            try :
                proVendor = ProductVendor.objects.filter(vendorId=1, isLive = True ,deleteProVendor= False,product=product,isStock = True).annotate(Min('sellPrice')).order_by('sellPrice').first()
                
                combValues = CombinationValues.objects.filter(proCombId = proVendor.proVarId,delete = False,isLive = True)
                
                values = []
                for combValue in combValues:
                    values.append(combValue.variantValue.varValue)

                try:
                    offerPro = OfferProductVendors.objects.get(
                        proVendorId = proVendor,
                        deleteOfferPro = False , 
                        isLive = True ,
                        offerId__deleteOffer = False,
                        offerId__isLive = True,
                        offerId__startDate__lte = datetime.datetime.now(),
                        offerId__endDate__gte = datetime.datetime.now()
                        )
                
                    return ({
                        "id" : proVendor.proVarId.pk,
                        "values" : values,
                        "sellPrice" : proVendor.sellPrice,
                        "offerPrice" : offerPro.offerPrice,
                        "isStock" : proVendor.isStock
                    })

                except:

                    return ({
                        "id" : proVendor.proVarId.pk,
                        "values" : values,
                        "sellPrice" : proVendor.sellPrice,
                        "offerPrice" : None,
                        "isStock" : proVendor.isStock
                    })

            except:
                return {}

    def get_variants(self,product):

        if product.hasVariants:
            
            try:    
                pcs = ProductCombinations.objects.filter(product = product,deleteComb = False)
                variants = []

                combValues = CombinationValues.objects.filter(proCombId = pcs.first(), delete = False, isLive = True)
                i = 0
                for combValue in combValues:

                    values = []
                    j=0

                    for pc in pcs:

                        combVals = CombinationValues.objects.filter(proCombId = pc, delete = False, isLive = True)
                        if len(values) is not 0:
                            if values[-1] == combVals[i].variantValue.varValue:
                                j += 1
                            else:
                                values.append(combVals[i].variantValue.varValue)
                        else:
                            values.append(combVals[i].variantValue.varValue)

                        j += 1


                    variants.append({
                            "title": combValue.variantValue.varId.variantTitle,
                            "values" : list(OrderedDict.fromkeys(values))
                        })

                    i += 1

                return variants
            except:
                return []

        return []

    def get_hasVariants (self,product):

        return product.hasVariants

    def get_combinations (self,product):

        if product.hasVariants:

            try:
                pcs = ProductCombinations.objects.filter(product = product,deleteComb = False)
                
                ser = ProductCombinationDetSerializer(instance = pcs , many =True)
                
                return ser.data

            except:

                return []

        return []

    def get_reviews (self,product):

        try:
            reviews = Review.objects.filter(productId = product,deleteReview = False,isLive = True)
            review_list = []
            for review in reviews:
                review_list.append({
                    "customerName" : review.customer.name,
                    "review" : review.review,
                    "stars" : review.stars,
                    "subject" : review.subject,
                })

            return review_list
        except:
            return []

    def get_description(self,product):

        return product.productDesc

    def get_brand (self,product):

        return product.brandId.brandTitle

    def get_category(self,product):

        return product.catId.catTitle

    def get_productCat(self,product):

        return product.proCatId.proCatTitle

    def get_price (self,product):

        if not product.hasVariants:
            try:
                proVendor = ProductVendor.objects.get(vendorId = 1,product = product, deleteProVendor = False , isLive = True)
                try:
                    offerPro = OfferProductVendors.objects.get(
                        proVendorId = proVendor,
                        deleteOfferPro = False , 
                        isLive = True ,
                        offerId__deleteOffer = False,
                        offerId__isLive = True,
                        offerId__startDate__lte = datetime.datetime.now(),
                        offerId__endDate__gte = datetime.datetime.now()
                        )
                    return {
                        "sellPrice":proVendor.sellPrice,
                        "isStock" : proVendor.isStock,
                        "offerPrice" : offerPro.offerPrice
                    }
                except:
                    return {
                        "sellPrice":proVendor.sellPrice,
                        "isStock" : proVendor.isStock,
                        "offerPrice" : None
                    }
            except:
                return    
        return
    
    def get_related (self,product):

        try:
            relatedProducts = Products.objects.filter(proCatId = product.proCatId)
            ser = FeatureProductSerializer(instance = relatedProducts,many=True, context = {'request':self.context.get('request')})
            return ser.data
        except:
            return []

        