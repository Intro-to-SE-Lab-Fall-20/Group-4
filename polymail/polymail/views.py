from django.conf import settings
import django.contrib.auth as auth
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import EmailForm, SearchForm
from . import models

def index(request):
    if request.user.is_authenticated:
        creds = models.UserProfile.get_google_credentials(request)
        service = models.create_service_if_necessary(creds)

        if service is None:
            raise ValueError('Could not create Gmail API')

    if request.method == 'GET':
        form = SearchForm()
        service = settings._GMAIL_SERVICE
        if (service is not None):
            messages = models.get_inbox(service, user_id='me')
    else:
        form = SearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            # TODO: search for relevant emails and display in index
            return redirect('/')
    return render(request, 'main/index.html', {"form":form})

def compose(request):
    if request.method == 'GET':
        form = EmailForm()
    else:
        form = EmailForm(request.POST)

        if form.is_valid():
            to_email = form.cleaned_data['to_email']
            subject = form.cleaned_data['subject']
            cc = form.cleaned_data['cc']
            body = form.cleaned_data['body']
            # attachment = request.FILES['attachment']

            sender = 'me' # FIXME This needs to be the logged in user's email

            message = models.create_gmail_message(
                sender,
                to_email,
                cc,
                subject,
                body,
                attachment=None
            )

            service = settings._GMAIL_SERVICE
            if service is None:
                raise ValueError('service is None')

            sent = models.send_gmail_message(service, user_id='me', message=message)

            if not sent:
                raise Exception('Error occurred sending email')

            return redirect('/')

    return render(request, 'main/compose.html', {'form': form})

def logout(request):
    auth.logout(request)
    return redirect('/')

