from django.contrib.auth import logout
from django.shortcuts import redirect, render

def index(request):
    return render(request, 'main/index.html')

def compose(request):
    return render(request, 'main/compose.html')

def logout_view(request):
    logout(request)
    return redirect('/')
