from allauth.account.forms import SignupForm, LoginForm, ResetPasswordForm, ChangePasswordForm, ResetPasswordKeyForm
from django import forms
from django.core.validators import MaxValueValidator
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError
import re

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    first_name = forms.CharField(label='Имя', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    last_name = forms.CharField(label='Фамилия', max_length=50,
                                widget=forms.TextInput(attrs={'placeholder': 'Фамилия'}))
    phone_number = forms.IntegerField(label='Номер телефона', validators=[MaxValueValidator(99999999999)],
                                      widget=forms.TextInput(attrs={'placeholder': 'Телефон'}), required=False)
    city = forms.CharField(label='Город', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Город'}))
    address = forms.CharField(label='Адрес', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Адрес'}))

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            if visible.name == 'remember':
                visible.field.widget.attrs['class'] = 'custom-control-input'
            visible.label = None

class CustomChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.label = None


class CustomResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomResetPasswordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.label = None


class CustomResetPasswordKeyForm(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super(CustomResetPasswordKeyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.label = None
