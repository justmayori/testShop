from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import phonenumbers
from phonenumbers import is_valid_number, parse
from django.core.exceptions import ValidationError


class SignupForm(UserCreationForm):

    email = forms.EmailField(max_length=254, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        try:
            parsed_number = parse(phone_number)
            if not is_valid_number(parsed_number):
                raise ValidationError('Invalid phone number. Please enter a valid phone number.')

        except phonenumbers.NumberParseException:
            raise ValidationError('Invalid phone number format.')

        return phone_number

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

