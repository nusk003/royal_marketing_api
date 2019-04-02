from User.models import User,Verification
from rest_framework import authentication,exceptions
from django.contrib.auth.backends import ModelBackend

import datetime
import uuid

from django.conf import settings

class PhoneBackend (object):

    def create_user(self,phoneToken):

        
        user = User.objects.create_user(phone = phoneToken.phone,is_customer=True)
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
                    #timestamp__gte = timestamp_difference
                )
            except Verification.DoesNotExist:

                phoneToken = Verification.objects.get(pk=pk)
                phoneToken.attempts = phoneToken.attempts + 1
                phoneToken.save()
                raise phoneToken.DoesNotExist

            user = User.objects.filter(phone__iexact = phoneToken.phone).first()

        else:

            pass

        if not user:
            user = self.create_user(phoneToken)
            phoneToken.used = True
            phoneToken.save()
            return user
        return user
