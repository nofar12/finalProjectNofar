from django.db import models
from django.contrib.auth.models import AbstractUser
class UserProfile(models.Model):  #defining the structure user's database
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=25)

    def __str__(self):
        return f'Username: {self.username}, Email: {self.email}, Password: {self.password}'
