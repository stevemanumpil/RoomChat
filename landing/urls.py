from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index),
    path('login/',views.index),
    path('register/', views.register),
    path('save/',views.save),
    path('check/', views.check),
]
