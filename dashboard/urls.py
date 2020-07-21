from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('',views.index),
    path('panel/<str:username>', views.PanelView.as_view()),
    path('load/<str:username>', views.StoreView.as_view()),
    path('logout/', views.Logout),
    path('store/', views.StoreView.as_view()),
]