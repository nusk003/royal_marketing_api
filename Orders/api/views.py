from rest_framework.views import APIView
from Cart.api.serializer import GetCartSerializerForOrder
from Cart.models import Cart,CartProducts
from User.models import PromoCodes,UsedPromoCodes
from Cart.api.views import checkPromoCode 
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from Orders.models import Orders,OrderProducts
import datetime
from rest_framework.parsers import JSONParser
from Products.models import Offer,ProductVendor
from User.api.serializers import MyOrdersSerializer


class CreateOrder (APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def generateInvoiceNo(self,user):

        orders = Orders.objects.filter(customerId = user)
        noOfOrders = len(orders)+1
        date = datetime.datetime.today().day
        month = datetime.datetime.today().month

        return "%02d%02d%03d%03dSG" % (date,month,user.pk,noOfOrders)

    

    def post(self,request):

       
        cart = Cart.objects.get(customerId = request.user,deleteCart = False)
        cartSer = GetCartSerializerForOrder(instance = cart,many=False,context={'request': request})
        if len(cartSer.data['CartProducts']) is 0 :
            return Response({
                "success" : False,
                "message" : "Your Cart is Empty"
            })
        invoiceNo = self.generateInvoiceNo(user = request.user)
        
        checkPromo = checkPromoCode.checkPromoCode(None,request,request.data.get('promoCode'),cartSer.data['totalPrice'])
        discount = 0
        promoCodeId = None
        if checkPromo['success']:
            discount = checkPromo['discount']
            promoCodeId = PromoCodes.objects.get(pk=checkPromo['promoCodeId'])
            UsedPromoCodes.objects.create(customerId = request.user,promoCodeId = promoCodeId)

        order = Orders.objects.create(
            customerId = request.user,
            invoiceNo = invoiceNo,
            orderStatus = 0,
            deliverAddress = request.data.get('deliverAddress'),
            discountPrice = discount,
            promoCodeId = promoCodeId

            )

        
        #return Response("checkPromo")
        for cp in cartSer.data['CartProducts']:
            offerPrice = None
            offerId = None
            if cp['price']['offerId'] is not None:
                offerPrice = cp['price']['offerPrice']
                offerId = Offer.objects.get(pk=Offercp['price']['offerId']) 
                
            if cp['price']['isStock']:
                OrderProducts.objects.create(
                    orderId = order,
                    proVendorId = ProductVendor.objects.get(pk = cp['price']['proVendorId']),
                    qty = cp['qty'],
                    costPrice = cp['price']['costPrice'],
                    sellPrice=cp['price']['sellPrice'],
                    discountPrice = offerPrice,
                    offerProductVendorId = offerId 
                )

        CartProducts.objects.filter(cartId = cart).delete() 
        
        ser = MyOrdersSerializer(instance = order,many=False)
        
        return Response({
            "success":True,
            "message":"Order has been placed Successfully",
            "Order":ser.data
            
            })
            
       
        
        

       