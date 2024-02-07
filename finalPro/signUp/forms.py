from django import forms
from .models import UserProfile

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
