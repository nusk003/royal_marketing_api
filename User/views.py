from django.shortcuts import render
from User.models import User
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes



# Create your views here.
@permission_classes((permissions.AllowAny,))
class adminLoginView (APIView):

    def post(self,request):

        
        userName = request.data.get('username', False)

        password = request.data.get('password', False)

       


   # exit

        user = authenticate(username = userName , password = password)

        if user is not None:
            if user.is_staff and user.is_superuser and user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token':token.key
                })
            else:
                raise Exception("Can't Login with given Credentials")
                
        else:

            raise Exception("Phone Number or Password is incorrect")
            
