from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.IntegerField()

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']
        