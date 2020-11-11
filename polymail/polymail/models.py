from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialApp, SocialAccount

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

import mimetypes

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio

import os

import base64
import dateutil.parser as parser


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

class Note(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('title',)

def create_service_if_necessary(creds):
    if settings._GMAIL_SERVICE is None:
        service = build('gmail', 'v1', credentials=creds)
        settings._GMAIL_SERVICE = service

    return settings._GMAIL_SERVICE

def create_gmail_message(sender, to, cc, subject, body, attachment_path):
    if attachment_path:
        message = _create_gmail_message_with_attachment(sender, to, cc, subject, body, attachment_path)
    else:
        message = MIMEText(body)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()

    return {'raw': raw}

def _create_gmail_message_with_attachment(sender, to, cc, subject, body, attachment_path):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    message.attach(MIMEText(body))

    content_type, encoding = mimetypes.guess_type(attachment_path)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'

    main, sub = content_type.split('/', 1)

    with open(attachment_path, mode='rb') as f:
        contents = f.read()

    if main == 'text':
        attach = MIMEText(contents, _subtype=sub)
    elif main == 'image':
        attach = MIMEImage(contents, _subtype=sub)
    elif main == 'audio':
        attach = MIMEAudio(contents, _subtype=sub)
    else:
        attach = MIMEBase(main, sub)
        attach.set_payload(contents)

    filename = os.path.basename(attachment_path)

    attach.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(attach)

    return message

def send_gmail_message(service, user_id, message):
    result = service.users().messages().send(userId=user_id, body=message).execute()

    return True

def get_inbox(service, user_id):
    results = service.users().threads().list(userId=user_id).execute()
    threads = results['threads']
    threads = threads[:10]
    messages_list = []
    for thread in threads:
        temp_dict = {}
        msg_id = thread['id']
        temp_dict['id'] = str(msg_id)
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

        messages_list.append(temp_dict)

    return messages_list

def get_specific_message(service, user_id, thread_id):
    temp_dict = {}
    temp_dict['id'] = thread_id
    msg = service.users().messages().get(userId=user_id, id=thread_id, format="full").execute()
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
    for four in header:
        if four['name'] == 'To':
            msg_to = four['value']
            temp_dict['To'] = msg_to
        else:
            pass
    temp_dict['Snippet'] = msg['snippet']
    try:
        msg_parts = payload['parts']
        part_one = msg_parts[1]
        part_body = part_one['body']
        part_data = part_body['data']
        msg_body = base64.urlsafe_b64decode(part_data)
        msg_body = msg_body.decode('utf-8')
        temp_dict['Body'] = msg_body
    except: 
        temp_dict['Body'] = msg['snippet']

    try:
        msg_parts = payload['parts']
        part_one = msg_parts[0]
        part_body = part_one['body']
        part_data = part_body['data']
        msg_body = base64.urlsafe_b64decode(part_data)
        msg_body = msg_body.decode('utf-8')
        temp_dict['PlainBody'] = msg_body
    except: 
        temp_dict['PlainBody'] = msg['snippet']

    return temp_dict
