import django.contrib.auth as auth
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from googleapiclient.discovery import build

from .models import UserProfile

def index(request):
    return render(request, 'main/index.html')

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
