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

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': _('Password')}),
        required=True)
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': _('Confirm Password')}),
        required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password1 != password2:
            raise forms.ValidationError(_('Passwords do not match'))
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get('password1')
        if password1:
            user.set_password(password1)
        if commit:
            user.save()
        return user


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
