from rest_framework import viewsets
from Products.api.serializers import VariantTypeSerializer,VariantValuesSerializer,ProductSerializer,ProductCombinationImagesSerializer,CreateVariantValueSerializer,FeatureProductSerializer,ProductDetailsSerializer
from Products.models import Variants,Products,VariantValues,ProductCombinationImages,ProductVendor,ProductCombinationKeywords
from rest_framework.permissions import IsAdminUser,AllowAny,IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import parsers,generics
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.db.models import Prefetch
from Products.api.paginations import LargeResultsSetPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from Products.models import Review


class VariantList (ListAPIView):

    serializer_class = VariantTypeSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Variants.objects.all()
        variant = self.request.query_params.get('variant', None)
        if variant is not None:
            queryset = queryset.filter(variantTitle__icontains =  variant)
        return queryset

class ProductList (viewsets.ModelViewSet):

    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUser,)
    parser_classes = (parsers.MultiPartParser,parsers.FormParser,)

    def create(self, request):

        Combinations = []
        
        noOfCombs = request.data['noOfCombs']
        noOfProImages = request.data['noOfImages']
        noOfProKeywords = request.data['noOfKeywords']
        arrPrice = []
        arrKeywords = []
        arrImages = []
        noOfProAreas = request.data['noOfAreas']

        #return Response(int(noOfCombs))
        if request.data['hasVariant'] == "true":
            for x in range(int(noOfCombs)):
                arrPrice = []
                arrKeywords = []
                arrImages = []
                arrCombValues = []
                noOfAreas = request.data['noOfAreas']
                noOfImages = request.data['Combinations[%d][noOfImages]' % x] 
                noOfKeywords = request.data['Combinations[%d][noOfKeywords]' % x]
                noOfVariants = request.data['noOfVariants']
                for y in range(int(noOfAreas)):
                    arrPrice.append({
                        "vendorId" : request.data['Combinations[%d][prices][%d][vendorId]' % (x,y)],
                        "costPrice" :request.data['Combinations[%d][prices][%d][costPrice]' % (x,y)],
                        "sellPrice" :request.data['Combinations[%d][prices][%d][sellPrice]' % (x,y)]
                    })
                for y in range(int(noOfImages)):
                    arrImages.append({
                        "proVarImg" : request.data['Combinations[%d][Images][%d][proVarImg]' % (x,y)],
                        "deleteImg" : request.data['Combinations[%d][Images][%d][deleteImg]' % (x,y)]
                    })
                for y in range(int(noOfKeywords)):
                    arrKeywords.append({
                        "keyword" : request.data['Combinations[%d][Keywords][%d][keyword]' % (x,y)],
                        "deleteKeyword" : request.data['Combinations[%d][Keywords][%d][deleteKeyword]' % (x,y)]
                    })
                for y in range(int(noOfVariants)):
                    arrCombValues.append({
                        "variantValue" : request.data['Combinations[%d][combValues][%d][variantValue]' % (x,y)],
                        "isLive" :request.data['Combinations[%d][combValues][%d][isLive]' % (x,y)],
                        "delete" :request.data['Combinations[%d][combValues][%d][delete]' % (x,y)]                    
                    })

                Combinations.append({
                    "prices":arrPrice,
                    "Keywords": arrKeywords,
                    "Images" : arrImages,
                    "combValues" : arrCombValues
                })
        else:
            for x in range(int(noOfProImages)):
                arrImages.append({
                    "proVarImg" : request.data['Images[%d][proVarImg]' % x],
                    "deleteImg" : request.data['Images[%d][deleteImg]' % x]
                })
            for x in range(int(noOfProAreas)):
                arrPrice.append({
                    "vendorId" : request.data['prices[%d][vendorId]' % x],
                    "costPrice" :request.data['prices[%d][costPrice]' % x],
                    "sellPrice" :request.data['prices[%d][sellPrice]' % x]
                })
            
            for x in range(int(noOfProKeywords)):
                arrKeywords.append({
                    "keyword" : request.data['Keywords[%d][keyword]' % x],
                    "deleteKeyword" : request.data['Keywords[%d][deleteKeyword]' % x]
                })
        

        product = {
            
            "Combinations": Combinations,
            "productTitle": request.data['productTitle'],
            "productDesc": request.data['productDesc'],
            "hasVariants": request.data['hasVariant'],
            "catId": request.data['catId'],
            "brandId": request.data['brandId'],
            "proCatId": request.data['proCatId'],
            "Images" : arrImages,
            "Keywords" : arrKeywords,
            "prices" : arrPrice

        }

        #return Response(len(product[Combinations]))

        serializer = self.get_serializer(data=product)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()



#@permission_classes((permissions.AllowAny,))
class ProductLists (generics.CreateAPIView):
    
    permission_classes = (IsAdminUser,)
    serializer_class = ProductSerializer
    parser_classes = (parsers.FormParser,parsers.MultiPartParser, parsers.FileUploadParser, )

    def perform_create(self, serializer):
            print(self.request.FILES['product'])
            serializer.save()


class VariantValueList (ListAPIView):

    serializer_class = VariantValuesSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):

        queryset = VariantValues.objects.all()
        variant = self.request.query_params.get('variant',None)
        searchQ = self.request.query_params.get('query',None)

        if variant is not None and searchQ is not None:
            queryset = queryset.filter(varId = variant,varValue__icontains=searchQ)
        return queryset


class UploadImage(viewsets.ModelViewSet):

    queryset = ProductCombinationImages.objects.all()
    serializer_class = ProductCombinationImagesSerializer
    permission_classes = (permissions.AllowAny,)
    parser_classes = (parsers.FormParser,parsers.MultiPartParser, parsers.FileUploadParser, )


class CreateVariantView (viewsets.ModelViewSet):

    queryset = Variants.objects.all()
    serializer_class = VariantTypeSerializer
    permission_classes = (IsAdminUser,)

class CreateVariantValueView (viewsets.ModelViewSet):

    queryset = VariantValues.objects.all()
    serializer_class = CreateVariantValueSerializer
    permission_classes = (IsAdminUser,)

    def create(self,request):

        noOfValues = int(request.data.get('noOfValues'))
        varId = int(request.data.get('varId'))
        array = []

        for x in range(noOfValues):
            tempData = {
                "varId":varId,
                "varValue":request.data.get('varValues[%d][value]' % x),
                "deleteVarValue" : False
            }

            serializer = self.get_serializer(data=tempData)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            array.append(serializer.data)

        return Response(array, status=status.HTTP_201_CREATED, headers=headers)    

    def perform_create(self, serializer):
        serializer.save()
    

class FeatureProductListView (ListAPIView):

    queryset = Products.objects.filter(deletePro = False,isLive = True)[:15]
    serializer_class = FeatureProductSerializer
    permission_classes = (AllowAny,)

    
class ProductDetailsView (ListAPIView):

    serializer_class = ProductDetailsSerializer
    permission_classes = (AllowAny,)

    def get_queryset (self):

        id = self.request.query_params.get('pid',None)
        try:
            queryset = Products.objects.filter(pk=id)
            return queryset
        except:
            return Response ({
                "success" :False,
                "message" : "product doesn't exist "  
            })

class SearchSuggestionsView (ListAPIView):

    queryset = Products.objects.filter(deletePro = False,isLive = True)
    serializer_class = FeatureProductSerializer
    permission_classes = (AllowAny,)
    pagination_class = LargeResultsSetPagination 
    filter_backends = (filters.SearchFilter,)
    search_fields = ('productTitle', 'Keywords__keyword','brandId__brandTitle','catId__catTitle','proCatId__proCatTitle',)

class ProductsForCategoryView (ListAPIView):

    queryset = Products.objects.filter(deletePro = False,isLive = True)
    serializer_class = FeatureProductSerializer
    permission_classes = (AllowAny,)
    pagination_class = LargeResultsSetPagination 
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('catId','brandId','proCatId','prices__Offers__offerId')


class CreateReviewView (APIView):

    permission_classes = (IsAuthenticated,)

    def post(self,request):

        productId = request.data.get('productId')
        review = request.data.get('review')
        subject = request.data.get('subject')
        stars = request.data.get('stars')

        try:
            product = Products.objects.get(pk=productId)

        except:
            return Response ({
            "success" : False,
            "message" : "Invalid Product"
        })
        
        try:
            reviewObj = Review.objects.create(productId = product ,review=review,customer = request.user,subject=subject,stars = int(stars))
            return Response ({
                "success" : True,
                "message" : "Review Successfully Created"
            })

        except :
            return Response ({
                "success" : False,
                "message" : "Review Created Failed"
            })

        