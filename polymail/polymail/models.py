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
import time
import dateutil.parser as parser
from datetime import datetime
from bs4 import BeautifulSoup

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

def get_inbox(service, user_id):
    results = service.users().threads().list(userId=user_id).execute()
    threads = results['threads']
    messages_list = []
    for thread in threads:
        temp_dict = {}
        msg_id = thread['id']
        msg = service.users().messages().get(userId='me', id=msg_id).execute()
        payload = msg['payload']
        header = payload['headers']

        for one in header:
            if one['name'] == 'Subject':
                msg_subject = one['value']
                temp_dict['Subject'] = msg_subject
            else:
                pass

        for two in header:
            if two['name'] == 'Date':
                msg_date = two['value']
                date_parse = (parser.parse(msg_date))
                m_date = (date_parse.date())
                temp_dict['Date'] = str(m_date)
            else:
                pass

        for three in header:
            if three['name'] == 'From':
                msg_from = three['value']
                temp_dict['Sender'] = msg_from
            else:
                pass

        temp_dict['Snippet'] = msg['snippet']

        try:
            msg_parts = payload['parts']
            part_one = msg_parts[0]
            part_body = part_one['body']
            part_data = part_body['data']
            clean_one = part_data.replace("-","+")
            clean_one = clean_one.replace("_","/")
            clean_two = base64.b64decode(bytes(clean_one, 'UTF-8'))
            soup = BeautifulSoup(clean_two, 'lxml')
            msg_body = soup.body()
            temp_dict['Body'] = msg_body
        except: 
            pass

        messages_list.append(temp_dict)

    return messages_list

        
    
    return snippets
