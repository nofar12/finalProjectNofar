from django.urls import path
from . import views
from signUp.views import signUp_user

urlpatterns = [
    path('', views.home1, name='page'),
    path('signUp/', signUp_user, name='signUp'),
]
