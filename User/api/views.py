from User.api.serializers import AreaSerializer,CreateOTPSerializer,ValidateOTPSerializer,MyProfileSerializer,UpdateNameSerializer,MyOrdersSerializer,EditAddress,DeleteAddress,AddAddress
from User.models import Area,Verification,User,UserAddress
from Orders.models import Orders,OrderProducts

from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,ListAPIView
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from django.contrib.auth import authenticate,login
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
import requests
from django.conf import settings
from rest_framework_api_key.permissions import HasAPIAccess
import datetime
import hashlib
import os




class AreaList (viewsets.ModelViewSet):

    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = (IsAdminUser,)


class SendVerificationCode (CreateAPIView):

    queryset = Verification.objects.all()
    serializer_class = CreateOTPSerializer
    permission_classes = (AllowAny,)


    def sendOTP (self,phone,message,otp):
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        otps = Verification.objects.filter(phone=phone, timestamp__range=(today_min, today_max))

        if otps.count() <= getattr(settings,'PHONE_LOGIN_ATTEMPTS',10):

            phoneToken = Verification.objects.create(phone=phone,otp=otp)
            #Setup the API params
            user_id = getattr(settings,'SMS_USER_ID','10310')
            api_key = getattr(settings,'SMS_API_KEY','d85rFVboHVgsqoDEwPFm')
            sender_id = getattr(settings,'SMS_SENDER_ID','Shoppingo')
            phoneNo = phone[1:]

            link = "https://app.notify.lk/api/v1/send?user_id="+user_id+"&api_key="+api_key+"&sender_id=Shoppingo&to="+phoneNo+"&message="+message
            requests.get(link)
            return phoneToken

        else:
            return False

    def generateOTP (self,length=4):
        
        hash_algorithm = getattr(settings, 'PHONE_LOGIN_OTP_HASH_ALGORITHM', 'sha256')
        m = getattr(hashlib, hash_algorithm)()
        m.update(getattr(settings, 'SECRET_KEY', None).encode('utf-8'))
        m.update(os.urandom(16))
        otp = str(int(m.hexdigest(), 16))[-length:]
        return otp

    def getMessage (self,name="Guest",otp=0):

        message = "Hi "+name+" Your otp code is "+otp+" and I'm coming from Python"
        return message
        
    def post(self,request):

        ser = self.serializer_class(
            data = request.data,
            context = {'request':request}
        )

        
        if ser.is_valid():
            phone = request.data.get('phone')
            phoneNo = str(phone)
            user = User.objects.filter(phone__iexact = phone).first()
            message = ""
            otp = self.generateOTP()
            if user :
                message = self.getMessage(name=user.name,otp=otp)
            else:
                message = self.getMessage(otp=otp)

            phoneToken = self.sendOTP(phone=phoneNo,message=message,otp=otp)

            if phoneToken:
                token_ser = self.serializer_class(
                    phoneToken,context={'request': request}
                )
                return Response({
                    "success":True,
                    "message":"Message sent successfully",
                    "data":token_ser.data
                    
                })
            return Response({
                'success' : False,
                'message': "you can not have more than {n} attempts per day, please try again tomorrow".format(
                    n=getattr(settings, 'PHONE_LOGIN_ATTEMPTS', 10))}, )

        else:
            return Response({
                "success":False,
                "message":"Please Enter a valid Phone number"
            })


class ValidateOTP (CreateAPIView):

    queryset = Verification.objects.all()
    serializer_class = ValidateOTPSerializer
    permission_classes = (AllowAny,)

    def create_user(self,phoneToken):

        user = User.objects.create_user(phone = phoneToken.phone,is_customer=True,is_staff=False)
        return user

    def get_user(self, user_id):
       try:
          return User.objects.get(pk=user_id)
       except User.DoesNotExist:
          return None

    def authenticate(self,pk=None,otp=None,email=None,password=None,**extra_fields):

        if not password:
            timestamp_difference = datetime.datetime.now() - datetime.timedelta(
             minutes=getattr(settings, 'PHONE_LOGIN_MINUTES', 10)
            )

            try:
                phoneToken = Verification.objects.get(
                    pk = pk,
                    otp = otp,
                    used = False,
                    timestamp__gte =  timestamp_difference
                )
            except Verification.DoesNotExist:

                phoneToken = Verification.objects.get(pk=pk)
                phoneToken.attempts = phoneToken.attempts + 1
                phoneToken.save()
                raise phoneToken.DoesNotExist

            user = User.objects.filter(phone__iexact = phoneToken.phone).first()
            if user :
                phoneToken.used = True
                phoneToken.save()
                return {
                    "isLogin":True,
                    "user":user
                }
            user = self.create_user(phoneToken=phoneToken)
            phoneToken.used = True
            phoneToken.save()
            return {
                    "isLogin":False,
                    "user":user
                }

        else:

            pass



    def post(self,request):

        ser = self.serializer_class(
            data = request.data,
            context = {'request':request}
        )

        if ser.is_valid():
            pk = request.data.get('pk')
            otp = request.data.get('otp')

            try:
                user = self.authenticate(pk=int(pk),otp=otp)
                token,created = Token.objects.get_or_create(user=user['user'])
                if user['isLogin']:
                    return Response({
                        "isLogin": True,
                        "token":token.key
                    })
                return Response({
                    "isLogin": False,
                    "token" : token.key
                })
                #timestamp_difference = datetime.datetime.now() - datetime.timedelta(
            # minutes=getattr(settings, 'PHONE_LOGIN_MINUTES', 10)
            #)
             #   return Response(timestamp_difference)

            except ObjectDoesNotExist:
                return Response(
                    {'reason': "OTP doesn't exist"},
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )

        return Response("Wrong")


class UpdateName(APIView):
    
    #queryset = User.objects.all()
    serializer_class = UpdateNameSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def put(self,request):
        
        ser = self.serializer_class(data = {"name":request.data.get('name')})
        if ser.is_valid():

            user = User.objects.get(pk=int(request.user.id))
            user.name = request.data.get('name')
            user.save()
            #serial = UserSerializer(user)
            return Response({
                "success" : True,
                "message":"updated Successfully"})
        return Response({
                "success" : False,
                "message":"Name is not Valid"})

class GetProfile (ListAPIView):

    serializer_class = MyProfileSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get (self,request):

        ser = self.serializer_class(instance = request.user,many=False)
        
        return Response(ser.data)

class MyOrdersView (ListAPIView):

    serializer_class = MyOrdersSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get (self,request):
        orders = Orders.objects.filter(customerId=request.user,deleteOrder = False)
        ser = self.serializer_class(instance = orders,many=True)
        return Response(ser.data)
    
class EditAddress (APIView):

    serializer_class = EditAddress
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def put(self,request):

        ser = self.serializer_class(data=request.data)
        if ser.is_valid():

            try:
                ua = UserAddress.objects.get(pk=request.data.get('id'),userId = request.user,deleteAddress = False)
                ua.address = request.data.get('address')
                ua.save()

                return Response({
                    "success" : True,
                    "message" : "Address Updated Successfully"
                })

            except:
                return Response({
                    "success" : False,
                    "message" : "Unauthorized"
                })


        return Response ({
            "success" : False,
            "message" : "Invalid Address"
        })

class DeleteAddress (APIView):

    serializer_class = DeleteAddress
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def put (self,request):

        ser = self.serializer_class(data=request.data)

        if ser.is_valid():
            
            try :
                ua = UserAddress.objects.get(pk = request.data.get('id'),userId = request.user)
                ua.deleteAddress = True
                ua.save()

                return Response ({
                    "success" : True,
                    "message" : "Address Successfully Deleted"
                })

            except:

                return Response({
                    "message" : False,
                    "message" : "Unauthorized"
                })

        return Response({
            "success" : False,
            "message" : "Invalid ID"
        })
        
class AddAddress (APIView):

    serializer_class = AddAddress
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self,request):

        ser = self.serializer_class(data = request.data)
        if ser.is_valid():

            try:
                ua = UserAddress.objects.create(userId = request.user,address = request.data.get('address'))
                return Response ({
                    "success" : True,
                    "message" : "Address Successfully Created"
                })

            except:
                return Response({
                    "message" : False,
                    "message" : "Unauthorized"
                })                

        return Response({
            "success" : False,
            "message" : "Invalid Address"
        })