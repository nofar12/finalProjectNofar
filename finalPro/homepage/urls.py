from django.urls import path
from . import views
from signUp.views import signUp_user
from findRecipe.views import findRecipe

urlpatterns = [
    path('', views.home, name='homepage'),
    path('signUp/', signUp_user, name='signUp'),
    path('findRecipe/', findRecipe, name='findRecipe'),
]
