from typing import Any
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User
from django.forms import fields
from django.utils.translation import ugettext_lazy as _

class LoginForm(auth_forms.AuthenticationForm):
    username = auth_forms.UsernameField(widget=forms.TextInput(
        attrs={
            'class': 'form-control', 
            'placeholder': 'maxmusterm', 
            'id': 'floatingUsername'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Passwort',
            'id': 'floatingPassword',
        }
    ))

    def __init__(self, request: Any, *args: Any, **kwargs: Any) -> None:
        super(__class__, self).__init__(request=request, *args, **kwargs)


class MyUserProfileEditForm(UserChangeForm):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(MyUserProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "Vorname"
        self.fields['last_name'].label = "Nachname"

    class Meta:
        model = User
        fields = ('first_name', 'last_name')

    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Vorname',
                'required': True
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Nachname',
                'required': True
            })
        }"""


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}), label='Altes Passwort')
    new_password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}), label='Neues Passwort')
    new_password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}), label='Neues Passwort wiederholen')

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
