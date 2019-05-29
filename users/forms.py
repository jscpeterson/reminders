from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm, forms.ModelForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('first_name', 'last_name', 'position', 'email', 'username')
        # TODO: Make the position field a dropdown
        # widgets = {
        #     'position': forms.Select(choices=CustomUser.POSITION_CHOICES, attrs={'class': 'form-control'}),
        # }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'position')
