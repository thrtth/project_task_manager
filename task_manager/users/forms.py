from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class CustomUserForm(forms.ModelForm):
    password_confirm = forms.CharField(
        label=_('Password Confirm'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Confirm Password')}),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Username')}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('First name')}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Last name')}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Password')}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', _('Passwords do not match'))
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label=_('Username'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Username')}),
    )

    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Password')}),
    )
