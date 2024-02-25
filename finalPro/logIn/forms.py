from django import forms
from .models import UserProfile

class UserLogInForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username or email', 'password']

