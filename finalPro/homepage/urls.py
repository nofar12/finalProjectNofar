# homepage/urls.py
from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name='home'),
    path('', views.home1, name='page'),
    path('home', views.home2, name='page'),

]
