from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index),
    path('logout/', views.logout),
    path('compose/<str:thread_id>/', views.compose, name="compose"),
    path('emailview/<str:thread_id>/', views.emailview, name="emailview"),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('polynotes/', views.polynotes, name="polynotes"),
    path("delete_note/<int:note_id>/", views.delete_note, name="delete_note")
]
