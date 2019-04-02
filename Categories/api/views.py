from rest_framework import viewsets
from Categories.api.serializers import CategorySerializer,BrandSerializer,ProductCategorySerializer,CategoryCreateSerializer,ProductCatCreateSerializer,BrandCreateSerializer,PopularBrandSerializer,CategoryListSerializer
from Categories.models import Categories,Brands,ProductCategories
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser,AllowAny
from rest_framework.response import Response
from rest_framework import status,parsers
from rest_framework_api_key.permissions import HasAPIAccess


class TopCategoriesList(ListAPIView):

    queryset = Categories.objects.all().order_by('?')[:3]
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)

class BrandList(viewsets.ModelViewSet):

    queryset = Brands.objects.all()
    serializer_class = BrandSerializer

class SearchProCatList(ListAPIView):

    serializer_class = ProductCategorySerializer
    permission_classes = (IsAdminUser,)

    def get_queryset (self):
        queryset = ProductCategories.objects.all()
        pcat = self.request.query_params.get('pcat',None)
        if pcat is not None :
            queryset = queryset.filter(proCatTitle__icontains = pcat)
        return queryset

class SearchBrandList (ListAPIView):

    serializer_class = BrandSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset (self):
        queryset = Brands.objects.all()
        brand = self.request.query_params.get('brand',None)
        if brand is not None :
            queryset = queryset.filter(brandTitle__icontains = brand)
        return queryset

class SearchCategoryList (ListAPIView):

    serializer_class = CategorySerializer
    permission_classes = (IsAdminUser,)

    def get_queryset (self):
        queryset = Categories.objects.all()
        cat = self.request.query_params.get('cat',None)
        if cat is not None :
            queryset = queryset.filter(catTitle__icontains = cat)
        return queryset

class CreateCategoryView (viewsets.ModelViewSet):

    queryset = Categories.objects.all()
    serializer_class = CategoryCreateSerializer
    permission_classes = (IsAdminUser,)
    parser_classes = (parsers.MultiPartParser,parsers.FormParser,)


    def create (self,request):

        noOfCatImages = request.data['noOfCatImages']
        catImages = []
        for x in range(int(noOfCatImages)):
            catImages.append({
                "catImg" : request.data['catImages[%d][catImg]' % x ],
                "deleteImg" : request.data['catImages[%d][deleteImg]' % x]
            })
        
        category = {
            "catTitle" : request.data['catTitle'],
            "CatImages" : catImages,
            "catDesc" : request.data['catDesc'],
            "deleteCat" : request.data['deleteCat']
        }

        serializer = self.get_serializer(data=category)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class CreateProductCategoryView (viewsets.ModelViewSet):
    
    queryset = ProductCategories.objects.all()
    serializer_class = ProductCatCreateSerializer
    permission_classes = (IsAdminUser,)

    def create(self,request):

        noOfCatImages = request.data['noOfCatImages']
        pCatImages = []
        for x in range(int(noOfCatImages)):
            pCatImages.append({
                "proCatImg" : request.data['catImages[%d][catImg]' % x ],
                "deleteImg" : request.data['catImages[%d][deleteImg]' % x]
            })
        
        proCategory = {
            "proCatTitle" : request.data['catTitle'],
            "proCatImages" : pCatImages,
            "proCatDesc" : request.data['catDesc'],
            "deleteProCat" : request.data['deleteCat'],
            "catId" : request.data['catId']
        }

        serializer = self.get_serializer(data=proCategory)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class CreateBrandView (viewsets.ModelViewSet):
    
    queryset = Brands.objects.all()
    serializer_class = BrandCreateSerializer
    permission_classes = (IsAdminUser,)

    def create(self,request):

        noOfCatImages = request.data['noOfCatImages']
        brandImages = []
        for x in range(int(noOfCatImages)):
            brandImages.append({
                "brandImg" : request.data['catImages[%d][catImg]' % x ],
                "deleteImg" : request.data['catImages[%d][deleteImg]' % x]
            })
        
        proCategory = {
            "brandTitle" : request.data['catTitle'],
            "brandImages" : brandImages,
            "brandDesc" : request.data['catDesc'],
            "deleteBrand" : request.data['deleteCat'],
           # "catId" : request.data['catId']
        }

        serializer = self.get_serializer(data=proCategory)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class PopularBrandsView (ListAPIView):

    queryset = Brands.objects.filter(deleteBrand = False)
    serializer_class = PopularBrandSerializer
    permission_classes = (AllowAny,)

class CategoryListView (ListAPIView):

    queryset = Categories.objects.filter(deleteCat = False)
    serializer_class = CategoryListSerializer
    permission_classes = (AllowAny,)