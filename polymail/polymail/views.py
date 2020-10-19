import django.contrib.auth as auth
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from googleapiclient.discovery import build

from .models import UserProfile

from polymail.forms import EmailForm, SearchForm

def index(request):
    if request.method == 'GET':
        form = SearchForm()
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
            attachment = request.FILES['attachment']
            # TODO: try except for sending email
            return redirect('/')
    return render(request, "main/compose.html", {"form":form})
        

def logout(request):
    auth.logout(request)
    return redirect('/')

def inbox(request):
    creds = UserProfile.get_google_credentials(request)

    # TOOD This needs to be created on login and stored elsewhere (as a global?)
    service = build('gmail', 'v1', credentials=creds)

    result = service.users().threads().list(userId='me').execute()
    threads = result['threads']

    for thread in threads:
        print(thread)

    return redirect('/')
