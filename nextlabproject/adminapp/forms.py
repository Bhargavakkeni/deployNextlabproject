from django import forms
from .models import LoginDetails

class LoginForm(forms.ModelForm):
    class Meta:
        model = LoginDetails
        fields = ['username', 'password']