from django.db import models
from django.contrib.auth.models import AbstractUser
class UserProfile(models.Model):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=25)
