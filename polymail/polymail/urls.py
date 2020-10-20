from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index),
    path('logout/', views.logout),
    path('compose/', views.compose),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls'))
]
