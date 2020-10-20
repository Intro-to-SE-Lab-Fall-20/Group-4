from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialApp, SocialAccount

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64

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

def create_service_if_necessary(creds):
    if settings._GMAIL_SERVICE is None:
        service = build('gmail', 'v1', credentials=creds)
        settings._GMAIL_SERVICE = service

    return settings._GMAIL_SERVICE

def create_gmail_message(sender, to, cc, subject, body, attachment):
    message = MIMEText(body)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    if attachment:
        print('Attachments are not yet supported but are in development')

    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()

    return {'raw': raw}

def send_gmail_message(service, user_id, message):
    result = service.users().messages().send(userId=user_id, body=message).execute()

    return True
