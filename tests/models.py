from phone_login.models import PhoneNumberAbstactUser


class CustomUser(PhoneNumberAbstactUser):
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username
