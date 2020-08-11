from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('',views.index),
    path('load/<str:name>', views.StoreView.as_view()),
    path('logout/', views.Logout),
    path('store/', views.StoreView.as_view()),
    path('check/', views.check),
]