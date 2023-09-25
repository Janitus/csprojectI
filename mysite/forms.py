from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        max_length=150,
        help_text="",
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text="",
    )

    class Meta:
        model = User
        fields = ("username", "password1")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']