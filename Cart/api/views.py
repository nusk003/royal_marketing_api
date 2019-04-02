from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import TokenAuthentication
from Cart.models import Cart,CartProducts
from Products.models import Products,ProductCombinations
from .serializer import AddToCartValidateSerializer,UpdateCartProSerializer,GetCartSerializer
from User.models import PromoCodes,UsedPromoCodes
from Cart.api.serializer import PromoCodeSerializer
import datetime
from decimal import Decimal


class AddtoCartView (APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = AddToCartValidateSerializer

    def addToCart(self,request,cart):

        try:
            product = Products.objects.get(pk=int(request.data.get('productId')))

        except:
            return {
                "success" : False,
                "message" : "ProductId is wrong"
            }

        if request.data.get('hasVariants') :
            try:
                pc = ProductCombinations.objects.get(pk=int(request.data.get('proVarId')))
                cp = CartProducts.objects.create(proVarId = pc,product = pc.product,qty=request.data.get('qty'),cartId=cart)
                cartSerializer = GetCartSerializer(instance = cart,many=False,context = {'request':request})
                return {
                    "success":True,
                    "message": "Product Added to cart successfully",
                    "cart" : cartSerializer.data
                }
            except:
                return {
                    "success" : False,
                    "message" : "Product CombinationId is wrong"
            }    
        
        cp = CartProducts.objects.create(product = product,qty=request.data.get('qty'),cartId=cart)
        cartSerializer = GetCartSerializer(instance = cart, many=False,context = {'request':request})

        return {
            "success":True,
            "message": "Product Added to cart successfully",
            "cart" : cartSerializer.data
        }

    def post(self,request):
        res = {}
        ser = self.serializer_class(data=request.data)
        if ser.is_valid() :

            cart = Cart.objects.get(customerId = request.user)
            if cart :
                res = self.addToCart(request,cart)
            else :
                cart = Cart.objects.create(customerId = request.user)
                res = self.addToCart(request,cart)

            return Response(res)
        res = {
            "success" : False,
            "message" : "Parameters not valid"
        }
        return Response(res)

class UpdateCartProView (APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = UpdateCartProSerializer

    def put (self,request):

        ser = self.serializer_class(data=request.data)

        if ser.is_valid():
            try:

                cart = Cart.objects.get(customerId = request.user)
                cp = CartProducts.objects.get(pk=request.data.get('cartProductId'),cartId=cart)
                cp.qty = request.data.get('qty')
                cp.save()
                cartSerializer = GetCartSerializer(instance = cart,many=False,context={'request':request})
                return Response({
                    "success" : True,
                    "message" : "Cart Updated Successfully",
                    "cart" : cartSerializer.data
                })

            except:
                return Response({
                    "success" : False,
                    "message" : "Cart Updated Failed"
                })

        return Response({
            "success" : False,
            "message" : "Parameter not valid"
        })


class GetCartView (ListAPIView):

    serializer_class = GetCartSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classess = (TokenAuthentication,)

    def get_queryset (self):

        queryset = Cart.objects.filter(customerId = self.request.user)[:1]
        return queryset


class DeleteCart (APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def put (self,request):

        try:

            cart = Cart.objects.get(customerId=request.user)
            try:
                cp = CartProducts.objects.get(pk=request.data.get('cartProductId'),cartId=cart)
                cp.delete()

                cartSerializer = GetCartSerializer(instance = cart,many=False,context={'request':request})

                return Response({
                    "success" : True,
                    "message" : "Cart Product Deleted Successfully",
                    "cart" : cartSerializer.data
                })
            except:

                return Response({
                    
                    "success": False,
                    "message" : "unauthorized user"
            })    

        except:

            return Response({
                "success" : False,
                "message" : "Invalid Cart"
            })

class checkPromoCode (APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def checkPromoCode (self,request,promoCode,cartTotal):
        try:
            pc = PromoCodes.objects.get(
                promoCode = promoCode,
                startDate__lte = datetime.datetime.now(),
                endDate__gte = datetime.datetime.now(),
                isLive = True,
                delete = False,
            )

        except:
            return {
                "success":False,
                "message": "Promocode Does not exist"
            }

        pc1 = {}  
            
        try:
            pc1 = PromoCodes.objects.get(pk=pc.pk, minPrice__lte = cartTotal)
            
        except:
            return {
                "success": False,
                "message" : "minimum Amount Should be Rs %.2f" % pc.minPrice
            }   

        try:
            used_pc = UsedPromoCodes.objects.get(
                promoCodeId = pc1,
                customerId = request.user
            )

            return {
                "success":False,
                "message": "You already used this code"
            }

        except:
            
            return {
                "success":True,
                "message" : "Promo Code Accepted",
                "discount" : pc1.discountValue,
                "promoCodeId" : pc1.promoCodeId
            }

    def post(self,request):

        data = self.checkPromoCode(request,request.data.get('promoCode'),request.data.get('cartTotal'))
        return Response(data)
          

class PromoCodeOffline (APIView):

    permission_classes = (AllowAny,)

    def post (self,request):

        try:
            pc = PromoCodes.objects.get(
                promoCode = request.data.get('promoCode'),
                startDate__lte = datetime.datetime.now(),
                endDate__gte = datetime.datetime.now(),
                isLive = True,
                delete = False,
            )
            try:
                pc1 = PromoCodes.objects.get(pk=pc.pk, minPrice__lte = request.data.get('cartTotal'))
                return Response({
                    "success": True,
                    "message" : "Promo Code Accepted",
                    "discount" : pc1.discountValue
                })
            except:
                return Response({
                    "success": False,
                    "message" : "minimum Amount Should be Rs %.2f" % pc.minPrice
                })

        except:
            return Response({
                "success":False,
                "message": "Promocode Does not exist"
            })


class MergeCart (APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self,request):


        cartProducts = request.data
        try:
            cart = Cart.objects.get(customerId = request.user,deleteCart = False)
        except:
            return Response({
                "success":False,
                "message" : "Invalid Cart"
            })
        for cp in cartProducts:
            
            if cp.get('hasVariants') :
                try:
                    proVarId = ProductCombinations.objects.get(pk=cp.get('proVarId'))
                    
                except:
                    
                    return Response({
                        "success":False,
                        "message" : "Invalid Product"
                    })
                try:
                    cartPro = CartProducts.objects.get(cartId = cart ,proVarId = proVarId)
                    cartPro.qty = cartPro.qty + int(cp.get('qty'))
                    cartPro.save()

                except:
                    CartProducts.objects.create(proVarId = proVarId,product=proVarId.product,qty=cp.get('qty'),cartId = cart)

            else:
                try:
                    product = Products.objects.get(pk=cp.get('id'))
                
                except:
                    return Response({

                        "success":False,
                        "message" : "Invalid Product"

                    })

                try:
                    cartPro = CartProducts.objects.get(cartId= cart ,product = product)
                    cartPro.qty = cartPro.qty + int(cp.get('qty'))
                    cartPro.save()
                
                except:
                    
                    CartProducts.objects.create(product=product,qty=cp.get('qty'),cartId = cart)
 
        return Response({
            "success" :True,
            "message" : "Cart Merged Successfully"
    })        



         

        
