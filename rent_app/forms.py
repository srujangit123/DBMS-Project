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


# class UpdateProfile(forms.ModelForm):
#     phoneno = models.CharField(blank=True, null=True)
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = CustomUser
#         fields = ('email', 'phoneno')

#     def clean_email(self):
#         email = self.cleaned_data.get('email')

#         if email and CustomUser.objects.filter(email=email).exclude(username=username).count():
#             raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
#         return email

#     def save(self, commit=True):
#         user = super(RegistrationForm, self).save(commit=False)
#         user.email = self.cleaned_data['email']

#         if commit:
#             user.save()

#         return user

class ProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        fields = (
            'phoneno',
            'profile_image',
            'upi_id',
            'address'
        )