from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialApp, SocialAccount
from google.oauth2.credentials import Credentials

def _on_delete(user):
    pass

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=_on_delete)

    def __unicode__(self):
        return ''

    class Meta:
        db_table = 'user_profile'
        app_label = 'main'

    def get_google_credentials(request):
        app = SocialApp.objects.get(provider='google')
        account = SocialAccount.objects.get(user=request.user)

        token = account.socialtoken_set.first().token
        refresh_token = account.socialtoken_set.first().token_secret

        client_key = app.client_id
        client_secret = app.secret

        scopes = settings.SOCIALACCOUNT_PROVIDERS['google']['SCOPE']

        creds = Credentials(
            token=token,
            refresh_token=refresh_token,
            client_id=client_key,
            client_secret=client_secret,
            scopes=scopes
        )

        return creds

    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)

            if len(result):
                return result[0].verified

        return False
