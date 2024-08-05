from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import (AuthenticationForm,
                                       UserCreationForm,
                                       UserChangeForm
                                       )
from django.utils.translation import gettext_lazy as _


class CustomUserCreateForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': _('Username')}),
        required=True)
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': _('First name')}),
        required=True)
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': _('Last name')}),
        required=True)

    class Meta:
        model = User
        fields = ['username',
                  'first_name',
                  'last_name',
                  'password1',
                  'password2'
                  ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Password')
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Confirm Password')
        })


class CustomUserUpdateForm(UserChangeForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': _('Username')}),
        required=True)
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': _('First name')}),
        required=True)
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': _('Last name')}),
        required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password']


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label=_('Username'),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Username')
            }),
    )

    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Password')
            }),
    )
