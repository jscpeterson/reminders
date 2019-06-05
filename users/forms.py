from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm, ModelForm):
    class Meta(UserCreationForm):

        model = CustomUser
        fields = ('first_name', 'last_name', 'position', 'email', 'username')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'position')
