from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('',views.LoginView.as_view()),
    path('login/',views.LoginView.as_view()),
    path('register/', views.RegisterView.as_view()),
]
