from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('',views.index),
    path('req/', views.req),
    path('logout/', views.Logout),
    path('get_message/', views.get_message),
]