from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    # email    = forms.EmailField()

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        # email    = self.cleaned_data.get('email')

        if username and password and email:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')

        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    email        = forms.EmailField(label='Email Address')
    email2       = forms.EmailField(label='Confirm email address')
    password     = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model    = User
        fields   = [
            'username',
            'email',
            'email2',
            'password'
        ]

    def clean_email(self):
        email    = self.cleaned_data.get('email')
        email2   = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError('Emails must match')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError('This email already exists')
        return email