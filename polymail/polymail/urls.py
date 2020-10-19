from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index),
    path('compose/', views.compose),
    path('logout/', views.logout_view),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls'))
]
