from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'contact_number']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'contact_number']
