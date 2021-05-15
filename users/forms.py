from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'user_name', 'upi_id', 'address', 'profile_image')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'user_name', 'upi_id', 'address', 'profile_image')


class ProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        fields = (
            'phoneno',
            'profile_image',
            'upi_id',
            'address'
        )
