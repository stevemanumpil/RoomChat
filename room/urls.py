from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index),
    path('auth/', include('landing.urls')),
    path('home/', include('dashboard.urls')),
    path('admin/', admin.site.urls),
]
