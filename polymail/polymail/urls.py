from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index),
    path('logout/', views.logout),
    path('compose/<str:thread_id>/', views.compose, name="compose"),
    path('emailview/<str:thread_id>/', views.emailview, name="emailview"),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls'))
]
