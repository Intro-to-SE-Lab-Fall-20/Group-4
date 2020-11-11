from django.conf import settings
import django.contrib.auth as auth
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import EmailForm, SearchForm
from . import models
from .models import Note

def index(request):
    messages = None
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
    return render(request, 'main/index.html', {"form":form, "messages": messages})

def compose(request, thread_id):
    if request.method == 'GET':
        if thread_id != '0':
            service = settings._GMAIL_SERVICE
            if (service is not None):
                message = models.get_specific_message(service, user_id='me', thread_id=thread_id)
                subject = message['Subject']
                sender = message['Sender']
                date = message['Date']
                to = message['To']
                body = ("\n\n\n--------Forwarded message--------\nFrom: " + sender 
                + "\nDate: " + date  + "\nSubject: " + subject + "\nTo: " + to + "\n\n")
                body += message['PlainBody']
                initial_dict = {
                    "subject":subject,
                    "body":body
                }
                form = EmailForm(initial=initial_dict)
            else:
                initial_dict = {
                    "subject":"service failed"
                }
                form = EmailForm(initial=initial_dict)
        else:
            initial_dict = {}
            form = EmailForm(initial=initial_dict)
    else:
        form = EmailForm(request.POST)

        if form.is_valid():
            to_email = form.cleaned_data['to_email']
            subject = form.cleaned_data['subject']
            cc = form.cleaned_data['cc']
            body = form.cleaned_data['body']
            attachment_path = form.cleaned_data['attachment']

            sender = 'me' # FIXME This needs to be the logged in user's email

            message = models.create_gmail_message(
                sender,
                to_email,
                cc,
                subject,
                body,
                attachment_path
            )

            service = settings._GMAIL_SERVICE
            if service is None:
                raise ValueError('service is None')

            sent = models.send_gmail_message(service, user_id='me', message=message)

            if not sent:
                raise Exception('Error occurred sending email')

            return redirect('/')

    return render(request, 'main/compose.html', {'form': form})

def emailview(request, thread_id):
    message = None
    service = settings._GMAIL_SERVICE
    if (service is not None):
        message = models.get_specific_message(service, user_id='me', thread_id=thread_id)

    return render(request, 'main/view-email.html', {"message": message})

def polynotes(request):
    note_id = int(request.GET.get('note_id', 0))
    notes = Note.objects.all()

    if request.method == 'POST':
        note_id = int(request.POST.get('note_id', 0))
        title = request.POST.get('title')
        content = request.POST.get('content', '')

        if note_id != 0:
            note = Note.objects.get(pk=note_id)
            note.title = title
            note.content = content
            note.save()

            return redirect('/polynotes/')

        else:
            note = Note.objects.create(title=title, content=content)

            return redirect('/polynotes/')

    if note_id > 0:
        note = Note.objects.get(pk=note_id)
    
    else:
        note = ''

    context = {
        'note_id': note_id,
        'notes': notes,
        'note': note
    }

    return render(request, 'main/polynotes.html', context)

def delete_note(request, note_id):
    note = Note.objects.get(pk=note_id)
    note.delete()

    return redirect('/polynotes/')

def logout(request):
    auth.logout(request)
    return redirect('/')

