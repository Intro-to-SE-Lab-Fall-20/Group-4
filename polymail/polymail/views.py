from django.contrib.auth import logout
from django.shortcuts import redirect, render

from polymail.forms import EmailForm

def index(request):
    return render(request, 'main/index.html')

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
            return redirect('/')
    return render(request, "main/compose.html", {"form":form})
        

def logout_view(request):
    logout(request)
    return redirect('/')
